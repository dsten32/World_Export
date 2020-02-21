scoreboard objectives add car-fuel dummy "car fuel extention"
scoreboard objectives add car-fuel2 dummy "car fuel extention"
scoreboard players add @e[type=witch] car-fuel 0
scoreboard players set @e[type=witch,scores={car-fuel=-1}] car-fuel 0
scoreboard players set @e[type=witch,scores={car-fuel=101}] car-fuel 100
scoreboard players add @a car-fuel 1
execute @a[scores={car-fuel=40}] ~ ~ ~ scoreboard players remove @e[type=witch,x=~,y=~1,z=~,dx=0,dy=0,dz=0] car-fuel 1
scoreboard players set @a[scores={car-fuel=40}] car-fuel 0
effect @e[type=witch,scores={car-fuel=!0}] slowness 0 0
effect @e[type=witch,scores={car-fuel=1}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=2}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=3}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=4}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=5}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=6}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=7}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=8}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=9}] slowness 9999 2 true
effect @e[type=witch,scores={car-fuel=0}] slowness 9999 100 true
scoreboard players set think car-fuel 10
execute @e[type=witch] ~ ~ ~ scoreboard players operation @s car-fuel2 = @s car-fuel
scoreboard players add @e[type=witch] car-fuel2 9
execute @e[type=witch] ~ ~ ~ scoreboard players operation @s car-fuel2 /= think car-fuel
execute @e[type=witch,scores={car-fuel2=0}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6§7██████████ §l§f|
execute @e[type=witch,scores={car-fuel2=1}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6█§7█████████ §l§f|
execute @e[type=witch,scores={car-fuel2=2}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6██§7████████ §l§f|
execute @e[type=witch,scores={car-fuel2=3}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6███§7███████ §l§f|
execute @e[type=witch,scores={car-fuel2=4}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6████§7██████ §l§f|
execute @e[type=witch,scores={car-fuel2=5}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6█████§7█████ §l§f|
execute @e[type=witch,scores={car-fuel2=6}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6██████§7████ §l§f|
execute @e[type=witch,scores={car-fuel2=7}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6███████§7███ §l§f|
execute @e[type=witch,scores={car-fuel2=8}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6████████§7██ §l§f|
execute @e[type=witch,scores={car-fuel2=9}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6█████████§7█ §l§f|
execute @e[type=witch,scores={car-fuel2=10}] ~ ~ ~ title @a[r=2] actionbar §l§f|§r §7Car Fuel §6██████████§7 §l§f|§r