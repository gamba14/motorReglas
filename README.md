# motorReglas
motor de reglas
### Como lo corro?
Instalar flask con pip o lo que sea
crear una variable de entorno
```bash
python3 ruleEngineResource.py
```
asumo que no estan usando linux
### ¿Qué es esto?
En principio analiza la forma de la regla, como primera aproximación tiene sentido. 
El resource solamente expone el parser a través de una API rest, se puede probar con cualquier cliente REST.

|El endpoint es|
|-----|
|/ruleEngine/create|

Enviarle un JSON con esta forma aproximadamente
```json
{
  "id": 1,
  "name": "myAwesomeRule1",
  "antecedents": [
    {
      "id1": 1,
      "op": ">",
      "vs": 24,
      "unit":"c°"
    },
    {
      "conector": "&&"
    },
    {
      "id1": 2,
      "op": "<",
      "vs": 22,
      "unit":"c°"
    }
  ],
  "consequences": [
    {
      "id2": 3,
      "action": "on"
    },
    {
      "conector": "&&"
    },
    {
      "id2": 4,
      "action": "off"
    }
  ]
}
```

1. Parseo de la regla.
Se debe analizar la sintáxis de la regla. En antecedentes, si existe un conector debe haber un antecedente que preceda al conector, mismo caso en los consecuentes. Es decir, verificar el balance de antecedentes y conectores. Si hay n conectores, debe haber n+1 antecedentes o consecuentes.
2. Verificación de la regla.
No tenemos que dar por hecho que todo lo que venga del front esté bien, por ejemplo, si alguien borra un sensor este podría aparecer en el cuadro de formación de las reglas. Para evitar estos problemas tenemos que verificar la semántica de la regla.
No solo tenemos que verificar que existan los id's de dispositivos, sino también debemos verificar que las unidades tengan sentido, no se puede admitir un valor de temperatura de 1000 °C. Verificar que no hayan contradicciones 
3. Persistencia de la regla.
La regla puede ser almacenada en una base relacional o en una base no SQL, léase mongoDB.
4. ABM de reglas.
El alta de la regla implica que esta deba ser digerida por el motor, una modificación en la regla también.

### Motor de reglas.
El motor de reglas puede ser un sencillo script de python, se podria integrar como un microservicio (ver el asunto de peticiones REST).
No debemos depender de llamadas sincrónicas (o no?). Se envían los datos recibidos al broker, estos datos son **id del dispositivo** y **la variable de proceso**, el motor digiere estos valores y analiza la entrada. Si se necesita de más de una entrada para evaluar una regla el motor espera a que llegue dicho valor, **la espera sólo bloquea al hilo donde se está evaluando la regla**. Una vez que se cuenta con todas las variables de proceso para ese actuador (qué pasa si tenemos una regla para id1 y otra regla necesita valores de id1 +id2 TODO, contemplar ese caso, timeout de lectura?) se procesará la regla, las variables **vs** siempre se comparan con **vp**, sean volts, ampere, fecha y hora, lúmenes, lo que sea, el motor tiene que poder compararlos y emitir juicio sobre la acción a tomar (prender/apagar, conectar/desconectar). 
Una vez emitido el juicio se deben enviar al broker **id2** + **va**, siendo **va** la variable de acción.
