# My-AppDaemon
My apps, my helpfiles, all about AppDaemon for Home Assistant

## Apps

* Adaptive heating control based on current temperature
* More advanced intent handling for google assistant
* Adaptive lighting control


https://community.home-assistant.io/t/howto-xiaomi-vacuum-zoned-cleaning/51293/22
https://community.home-assistant.io/t/howto-xiaomi-vacuum-zoned-cleaning/51293/37
https://community.home-assistant.io/t/howto-xiaomi-vacuum-zoned-cleaning/51293/39

{
  "entity_id": "vacuum.living_room_vacum",
  "command": "app_goto_target",
  "params": [23350,23600]
}


{
  "entity_id": "vacuum.living_room_vacum",
  "command": "app_goto_target",
  "params": [22600,22800]
}

vaccum_barnrum_go_and_clean_and_go_home:
    alias: "Go to childrens room, clean and then go home"
    sequence:
      # Go to starting point in the kids room
      - service: vacuum.send_command
        data:
          entity_id: vacuum.dammsugare
          command: app_goto_target
          params: [23350,23600]
      #Wait untill done
      - wait_template: "{{ states.vacuum.dammsugare.attributes.status == 'Idle'}}"
      - service: input_number.set_value
        data:
          entity_id: input_number.vaccum_progress
          value: 1
      - delay: '00:00:30'
      #clean room
      - service: vacuum.send_command
        data:
          entity_id: vacuum.dammsugare
          command: app_zoned_clean
          params: [[20613,19502,24163,25002,1]]
      #Wait untill done
      - wait_template: "{{ states.vacuum.dammsugare.attributes.status == 'Returning home'}}"
      - service: input_number.set_value
        data:
          entity_id: input_number.vaccum_progress
          value: 2
      - delay: '00:00:05'
      #Stop going home
      - service: vacuum.stop
        data:
          entity_id: vacuum.dammsugare
