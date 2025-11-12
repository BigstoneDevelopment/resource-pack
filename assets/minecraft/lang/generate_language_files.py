import json
import os

minecraft_languages = [
    "en_us", "en_gb", "de_de", "fr_fr", "es_es", "es_mx", "pt_br", "pt_pt",
    "ru_ru", "ja_jp", "zh_cn", "zh_tw", "ko_kr", "it_it", "nl_nl", "pl_pl",
    "tr_tr", "cs_cz", "da_dk", "fi_fi", "sv_se", "hu_hu", "ro_ro", "uk_ua",
    "el_gr", "he_il", "ar_sa", "th_th", "vi_vn", "id_id", "no_no", "sr_sp",
    "sk_sk", "hr_hr", "lt_lt", "lv_lv", "et_ee"
]

content = {
    "commands.trigger.add.success": "",
    "commands.trigger.set.success": "",
    "commands.trigger.simple.success": "",
    "menu.custom_options.tooltip": "",
    "menu.custom_screen_info.tooltip": "Exit Session",
    "menu.custom_screen_info.title": "Exit Session?",
    "menu.custom_screen_info.contents": "",
    "menu.custom_screen_info.disconnect": "Session Exited",
    "chat.link.warning": "",
    "chat.link.confirm": "󏿘󏻭Are you sure you want to open the following?",
    "selectWorld.backupQuestion.experimental": "󏿿",
    "selectWorld.backupWarning.experimental": "Welcome to Bigstone sandbox!\n\n\n\n\n\n\n\nIf you're seeing this while loading a bigstone datapack world that means\nyou have equipped the resourcepack and are ready to hop in.\n If this isn't a bigstone datapack world that means you loaded something else.\nRegardless have fun!",
    "selectWorld.backupJoinSkipButton": "Join World"
}

script_dir = os.path.dirname(os.path.abspath(__file__))

for lang in minecraft_languages:
    file_path = os.path.join(script_dir, f"{lang}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)