/**
 * Script de Google Apps para crear un quiz de Estadística con 25 preguntas
 * Cada pregunta tiene opciones múltiples con 6 posibles respuestas
 */

function crearQuizEstadistica() {
  // Obtener el formulario actual (el que está vinculado a este script)
  const form = FormApp.getActiveForm();
  
  // Limpiar preguntas existentes
  const items = form.getItems();
  items.forEach(item => form.deleteItem(item));
  
  // Configurar como quiz
  form.setIsQuiz(true);
  
  // Configurar opciones del formulario
  form.setTitle('Quiz de Estadística - 25 Preguntas');
  form.setDescription('Quiz sobre conceptos básicos de estadística. Cada pregunta vale 4 puntos.');
  form.setRequireLogin(false);
  form.setAllowResponseEdits(false);
  form.setAcceptingResponses(true);
  
  // Configurar para mostrar preguntas en orden aleatorio
  form.setShuffleQuestions(true);
  
  // Opciones de respuesta (la primera siempre será la correcta)
  const opciones = [
    '(ED) Estadística Descriptiva',
    '(EI) Estadística Inferencial', 
    '(VCC) Variable Cuantitativa Continua',
    '(VCD) Variable Cuantitativa Discreta',
    '(VCN) Variable Cualitativa Nominal',
    '(VCO) Variable Cualitativa Ordinal'
  ];
  
  // Array de 25 preguntas con sus respectivas respuestas correctas
  const preguntas = [
    {
      pregunta: 'Se recopilan datos sobre las edades de 100 estudiantes y se calcula la media aritmética para conocer la edad promedio del grupo.',
      respuestaCorrecta: 0 // ED
    },
    {
      pregunta: 'A partir de una muestra de 50 familias se quiere estimar el ingreso promedio de todas las familias de una ciudad.',
      respuestaCorrecta: 1 // EI
    },
    {
      pregunta: 'Se mide la temperatura corporal de pacientes en un hospital, registrando valores como 36.5°C, 37.2°C, 38.1°C.',
      respuestaCorrecta: 2 // VCC
    },
    {
      pregunta: 'Se cuenta el número de hijos por familia en un barrio: 0, 1, 2, 3, 4 hijos.',
      respuestaCorrecta: 3 // VCD
    },
    {
      pregunta: 'Se registra el color de ojos de los estudiantes: azul, verde, café, negro.',
      respuestaCorrecta: 4 // VCN
    },
    {
      pregunta: 'Se evalúa el nivel de satisfacción de clientes: muy insatisfecho, insatisfecho, neutral, satisfecho, muy satisfecho.',
      respuestaCorrecta: 5 // VCO
    },
    {
      pregunta: 'Se calcula la mediana y los cuartiles de los salarios de empleados de una empresa para describir la distribución.',
      respuestaCorrecta: 0 // ED
    },
    {
      pregunta: 'Con base en una muestra de votantes se predice el resultado de las elecciones presidenciales.',
      respuestaCorrecta: 1 // EI
    },
    {
      pregunta: 'Se registra el tiempo que tardan los estudiantes en resolver un examen: 45.3 min, 52.7 min, 38.9 min.',
      respuestaCorrecta: 2 // VCC
    },
    {
      pregunta: 'Se cuenta el número de automóviles que pasan por un peaje cada hora: 150, 200, 175 autos.',
      respuestaCorrecta: 3 // VCD
    },
    {
      pregunta: 'Se clasifica a los empleados por departamento: ventas, marketing, recursos humanos, contabilidad.',
      respuestaCorrecta: 4 // VCN
    },
    {
      pregunta: 'Se califica el desempeño de empleados: excelente, bueno, regular, malo.',
      respuestaCorrecta: 5 // VCO
    },
    {
      pregunta: 'Se elabora un histograma con las calificaciones finales de estudiantes para visualizar la distribución de notas.',
      respuestaCorrecta: 0 // ED
    },
    {
      pregunta: 'Se realiza una prueba de hipótesis para determinar si un nuevo medicamento es más efectivo que el tratamiento actual.',
      respuestaCorrecta: 1 // EI
    },
    {
      pregunta: 'Se mide la estatura de jugadores de básquetbol: 1.85m, 1.92m, 2.01m, 1.88m.',
      respuestaCorrecta: 2 // VCC
    },
    {
      pregunta: 'Se registra el número de goles anotados por partido en una liga: 0, 1, 2, 3, 4 goles.',
      respuestaCorrecta: 3 // VCD
    },
    {
      pregunta: 'Se clasifica a los pacientes por tipo de sangre: A, B, AB, O.',
      respuestaCorrecta: 4 // VCN
    },
    {
      pregunta: 'Se evalúa la intensidad del dolor en pacientes: sin dolor, leve, moderado, severo, insoportable.',
      respuestaCorrecta: 5 // VCO
    },
    {
      pregunta: 'Se calcula la desviación estándar de los pesos de productos manufacturados para evaluar la variabilidad del proceso.',
      respuestaCorrecta: 0 // ED
    },
    {
      pregunta: 'Se utiliza un intervalo de confianza del 95% para estimar la proporción de personas que apoyan una propuesta política.',
      respuestaCorrecta: 1 // EI
    },
    {
      pregunta: 'Se registra el peso de recién nacidos en un hospital: 2.8 kg, 3.2 kg, 3.5 kg, 2.9 kg.',
      respuestaCorrecta: 2 // VCC
    },
    {
      pregunta: 'Se cuenta el número de quejas recibidas por día en un centro de atención: 5, 8, 3, 12 quejas.',
      respuestaCorrecta: 3 // VCD
    },
    {
      pregunta: 'Se registra la marca de celular preferida por los consumidores: Apple, Samsung, Huawei, Xiaomi.',
      respuestaCorrecta: 4 // VCN
    },
    {
      pregunta: 'Se evalúa el nivel educativo de participantes: primaria, secundaria, preparatoria, licenciatura, posgrado.',
      respuestaCorrecta: 5 // VCO
    },
    {
      pregunta: 'Se construye un diagrama de barras para mostrar la frecuencia de accidentes por mes en una fábrica.',
      respuestaCorrecta: 0 // ED
    }
  ];
  
  // Crear cada pregunta del quiz
  preguntas.forEach((item, index) => {
    try {
      // Usar las opciones en el orden fijo especificado
      const opcionesParaPregunta = [...opciones];
      
      // Obtener el texto de la respuesta correcta
      const respuestaCorrectaTexto = opciones[item.respuestaCorrecta];
      
      // Crear la pregunta de opción múltiple
      const preguntaItem = form.addMultipleChoiceItem();
      
      // Establecer el título de la pregunta (asegurar que el texto no esté vacío)
      const textoPregunta = item.pregunta.trim();
      if (textoPregunta.length === 0) {
        throw new Error(`Pregunta ${index + 1} tiene texto vacío`);
      }
      
      preguntaItem.setTitle(textoPregunta);
      preguntaItem.setRequired(true);
      preguntaItem.setPoints(4);
      
      Logger.log(`Pregunta ${index + 1}: ${textoPregunta.substring(0, 50)}...`);
      Logger.log(`Respuesta correcta: ${respuestaCorrectaTexto}`);
    
    // Crear las opciones con retroalimentación
    const opcionesConFeedback = opcionesParaPregunta.map(opcion => {
      if (opcion === respuestaCorrectaTexto) {
        // Esta es la respuesta correcta
        return preguntaItem.createChoice(opcion, true);
      } else {
        // Esta es una respuesta incorrecta
        return preguntaItem.createChoice(opcion, false);
      }
    });
    
      // Establecer las opciones en la pregunta
      preguntaItem.setChoices(opcionesConFeedback);
      
    } catch (error) {
      Logger.log(`Error procesando pregunta ${index + 1}: ${error.message}`);
      Logger.log(`Texto de la pregunta: "${item.pregunta}"`);
      throw error;
    }
  });
  
  // Configurar opciones adicionales del quiz
  form.setConfirmationMessage('¡Gracias por completar el quiz de estadística! Tus respuestas han sido registradas.');
  form.setProgressBar(true);
  
  // Mostrar información del formulario modificado
  Logger.log('Formulario modificado exitosamente!');
  Logger.log('Se agregaron 25 preguntas de estadística.');
  Logger.log('URL del formulario: ' + form.getPublishedUrl());
  Logger.log('URL para editar: ' + form.getEditUrl());
  
  return form;
}

/**
 * Función auxiliar para mezclar un array
 */
function mezclarArray(array) {
  const arrayCopia = [...array];
  for (let i = arrayCopia.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arrayCopia[i], arrayCopia[j]] = [arrayCopia[j], arrayCopia[i]];
  }
  return arrayCopia;
}

/**
 * Función para obtener información del formulario actual
 */
function obtenerInfoFormulario() {
  const form = FormApp.getActiveForm();
  Logger.log('URL del formulario: ' + form.getPublishedUrl());
  Logger.log('URL para editar: ' + form.getEditUrl());
  Logger.log('Número de preguntas: ' + form.getItems().length);
}
