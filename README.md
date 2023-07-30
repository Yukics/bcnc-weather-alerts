# Alertas del tiempo

**Entrevista técnica BCNC**

## Requisitos previos

+ Docker
+ Discord

## Puesta en marcha

1. Clonar el repositorio

    ```powershell
    git clone https://github.com/Yukics/bcnc-weather-alerts.git
    ```

2. Configurar los parámetros descritos en el .env (`cp .env_tes .env`), se trata de el token de la api y url de [weatherapi.com](https://www.weatherapi.com/) y [webhook de Discord](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) al que mandaremos los mensajes. Y también configurar las reglas de alertas, ejemplo en `./conf/main.yaml` o más abajo en el readme.Además del [nivel de verbosity del log](https://docs.python.org/3/howto/logging.html#logging-levels:~:text=suit%20their%20requirements.-,Logging%20Levels,-%C2%B6).

3. Ejecutar

    ```powershell
    docker-compose up -d && docker-compose logs -f
    ```

4. Revisamos que todo esté funcionando correctamente, se enviará un mensaje de prueba a Discord y de haber errores aparecerán en los logs.

## Fichero de configuración

El fichero de configuración es una array en .yaml que describe la siguiente estructura:

```yaml
- name: Reglas Alejo # Nombre de la regla
  unit: "C" # C para celsius F para Farenheit
  location: "Palma" # Localización en la que desamos establecer las alertas
  alerts: # Los tipos de alerta configuradas: temperaturas máximas y mínimas, además de si va a llover hoy.
    max_temp: 30  
    min_temp: 14
    rain: true 
```

Con tal de afinar la localización deseada, os invito a hacer las pruebas a través de la herramienta de [weatherapi.com](https://www.weatherapi.com/api-explorer.aspx)

## Reference

+ [Wheather API Docs](https://www.weatherapi.com/docs/)
