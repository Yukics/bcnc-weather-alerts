import libs.logs as logs
import libs.conf as conf
import libs.api as api
import os
import logging
import time

def main():
    # Logging implementation
    logs.setupLogging()

    # Getting vars (example if needed to add defaults)
    env_vars = {
        "api_key": os.getenv('API_KEY') if os.getenv('API_KEY') else 'f5db08e472cb4b4fb5a191058233007',
        "webhook": os.getenv('DISCORD_WEBHOOK') if os.getenv('DISCORD_WEBHOOK') else 'https://discord.com/api/webhooks/1135292977342849127/AE1J-o917s3KVtTnu18KdUkYNRAIDUc17J5Nd3uBtG70yMN58Pdm8cVBYyK5qq22Lblm',
        "file": os.getenv('CONF_FILE') if os.getenv('CONF_FILE') else './conf/main.yaml',
        "check_rate": int(os.getenv('CHECK_RATE')) if os.getenv('CHECK_RATE') else 10
    }

    conf_loaded = conf.load(env_vars['file'])
    api.sendMessage(env_vars['webhook'], "[ALERTA] El bot de alertas meteorológicas ha sido configurado")

    while True:

        # If configuration file is changed it loads it "hot reloading"
        conf_is_changed = conf.load(env_vars['file'])
        if conf_loaded != conf_is_changed:
            conf_loaded = conf_is_changed
            logging.info("Current configuration has changed")


        for rule in conf_loaded:
            status = api.getForecast(env_vars['api_key'], rule['location'])
            
            # definition of temp units
            default_temp_unit = "temp_c"
            if rule['unit'] != "c" and rule['unit'] != "C":
                default_temp_unit = "temp_f"

            # max temps
            if status['current'][default_temp_unit] >= rule['alerts']['max_temp']:
                logging.info("Triggering max temp alert for rule {}".format(rule['name']))
                api.sendMessage(
                    env_vars['webhook'], 
                    "[ALERTA] La temperatura ha superado el umbral {0} actualmente para la localización {1} estamos a {2}º {3}".format(
                        rule['alerts']['max_temp'],
                        rule['location'],
                        status['current'][default_temp_unit],
                        rule['unit']
                        )
                )
            # min temps
            if status['current'][default_temp_unit] <= rule['alerts']['min_temp']:
                logging.info("Triggering min temp alert for rule {}".format(rule['name']))
                api.sendMessage(
                    env_vars['webhook'], 
                    "[ALERTA] La temperatura ha disminuido del umbral {0} actualmente para la localización {1} estamos a {2}º {3}".format(
                        rule['alerts']['min_temp'],
                        rule['location'],
                        status['current'][default_temp_unit],
                        rule['unit']
                        )
                )

            time.sleep(1) # Due to API ratelimit

            # rain
            if rule['alerts']['rain']:
                will_rain = api.willRain(status)
                if will_rain:
                    logging.info("Triggering rain alert for rule {}".format(rule['name']))
                    api.sendMessage(
                        env_vars['webhook'], 
                        "[ALERTA] Va a llover en {0} desde las {1} hasta {2}".format(
                            rule['location'],
                            will_rain[0],
                            will_rain[-1]
                        )
                    )

                    print(will_rain)

            time.sleep(1) # Due to API ratelimit

        time.sleep(env_vars['check_rate']-2)

if __name__ == '__main__':
    main()