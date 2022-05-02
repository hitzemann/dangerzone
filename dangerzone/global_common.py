import sys
import os
import inspect
import appdirs
import platform
import subprocess
import shutil
import json
import gzip
import colorama
from colorama import Fore, Back, Style

from .settings import Settings
from .container import convert


class GlobalCommon(object):
    """
    The GlobalCommon class is a singleton of shared functionality throughout the app
    """

    def __init__(self):
        # Version
        try:
            with open(self.get_resource_path("version.txt")) as f:
                self.version = f.read().strip()
        except FileNotFoundError:
            # In dev mode, in Windows, get_resource_path doesn't work properly for the container, but luckily
            # it doesn't need to know the version
            self.version = "unknown"

        # Initialize terminal colors
        colorama.init(autoreset=True)

        # App data folder
        self.appdata_path = appdirs.user_config_dir("dangerzone")

        # Container
        self.container_name = "hitzeman/dangerzone"

        # Languages supported by tesseract
        self.ocr_languages = {
            "Afrikaans": "ar",
            "Albanian": "sqi",
            "Amharic": "amh",
            "Arabic": "ara",
            "Arabic script": "Arabic",
            "Armenian": "hye",
            "Armenian script": "Armenian",
            "Assamese": "asm",
            "Azerbaijani": "aze",
            "Azerbaijani (Cyrillic)": "aze_cyrl",
            "Basque": "eus",
            "Belarusian": "bel",
            "Bengali": "ben",
            "Bengali script": "Bengali",
            "Bosnian": "bos",
            "Breton": "bre",
            "Bulgarian": "bul",
            "Burmese": "mya",
            "Canadian Aboriginal script": "Canadian_Aboriginal",
            "Catalan": "cat",
            "Cebuano": "ceb",
            "Cherokee": "chr",
            "Cherokee script": "Cherokee",
            "Chinese - Simplified": "chi_sim",
            "Chinese - Simplified (vertical)": "chi_sim_vert",
            "Chinese - Traditional": "chi_tra",
            "Chinese - Traditional (vertical)": "chi_tra_vert",
            "Corsican": "cos",
            "Croatian": "hrv",
            "Cyrillic script": "Cyrillic",
            "Czech": "ces",
            "Danish": "dan",
            "Devanagari script": "Devanagari",
            "Divehi": "div",
            "Dutch": "nld",
            "Dzongkha": "dzo",
            "English": "eng",
            "English, Middle (1100-1500)": "enm",
            "Esperanto": "epo",
            "Estonian": "est",
            "Ethiopic script": "Ethiopic",
            "Faroese": "fao",
            "Filipino": "fil",
            "Finnish": "fin",
            "Fraktur script": "Fraktur",
            "Frankish": "frk",
            "French": "fra",
            "French, Middle (ca.1400-1600)": "frm",
            "Frisian (Western)": "fry",
            "Gaelic (Scots)": "gla",
            "Galician": "glg",
            "Georgian": "kat",
            "Georgian script": "Georgian",
            "German": "deu",
            "Greek": "ell",
            "Greek script": "Greek",
            "Gujarati": "guj",
            "Gujarati script": "Gujarati",
            "Gurmukhi script": "Gurmukhi",
            "Hangul script": "Hangul",
            "Hangul (vertical) script": "Hangul_vert",
            "Han - Simplified script": "HanS",
            "Han - Simplified (vertical) script": "HanS_vert",
            "Han - Traditional script": "HanT",
            "Han - Traditional (vertical) script": "HanT_vert",
            "Hatian": "hat",
            "Hebrew": "heb",
            "Hebrew script": "Hebrew",
            "Hindi": "hin",
            "Hungarian": "hun",
            "Icelandic": "isl",
            "Indonesian": "ind",
            "Inuktitut": "iku",
            "Irish": "gle",
            "Italian": "ita",
            "Italian - Old": "ita_old",
            "Japanese": "jpn",
            "Japanese script": "Japanese",
            "Japanese (vertical)": "jpn_vert",
            "Japanese (vertical) script": "Japanese_vert",
            "Javanese": "jav",
            "Kannada": "kan",
            "Kannada script": "Kannada",
            "Kazakh": "kaz",
            "Khmer": "khm",
            "Khmer script": "Khmer",
            "Korean": "kor",
            "Korean (vertical)": "kor_vert",
            "Kurdish (Arabic)": "kur_ara",
            "Kyrgyz": "kir",
            "Lao": "lao",
            "Lao script": "Lao",
            "Latin": "lat",
            "Latin script": "Latin",
            "Latvian": "lav",
            "Lithuanian": "lit",
            "Luxembourgish": "ltz",
            "Macedonian": "mkd",
            "Malayalam": "mal",
            "Malayalam script": "Malayalam",
            "Malay": "msa",
            "Maltese": "mlt",
            "Maori": "mri",
            "Marathi": "mar",
            "Mongolian": "mon",
            "Myanmar script": "Myanmar",
            "Nepali": "nep",
            "Norwegian": "nor",
            "Occitan (post 1500)": "oci",
            "Old Georgian": "kat_old",
            "Oriya (Odia) script": "Oriya",
            "Oriya": "ori",
            "Pashto": "pus",
            "Persian": "fas",
            "Polish": "pol",
            "Portuguese": "por",
            "Punjabi": "pan",
            "Quechua": "que",
            "Romanian": "ron",
            "Russian": "rus",
            "Sanskrit": "san",
            "script and orientation": "osd",
            "Serbian (Latin)": "srp_latn",
            "Serbian": "srp",
            "Sindhi": "snd",
            "Sinhala script": "Sinhala",
            "Sinhala": "sin",
            "Slovakian": "slk",
            "Slovenian": "slv",
            "Spanish, Castilian - Old": "spa_old",
            "Spanish": "spa",
            "Sundanese": "sun",
            "Swahili": "swa",
            "Swedish": "swe",
            "Syriac script": "Syriac",
            "Syriac": "syr",
            "Tajik": "tgk",
            "Tamil script": "Tamil",
            "Tamil": "tam",
            "Tatar": "tat",
            "Telugu script": "Telugu",
            "Telugu": "tel",
            "Thaana script": "Thaana",
            "Thai script": "Thai",
            "Thai": "tha",
            "Tibetan script": "Tibetan",
            "Tibetan Standard": "bod",
            "Tigrinya": "tir",
            "Tonga": "ton",
            "Turkish": "tur",
            "Ukrainian": "ukr",
            "Urdu": "urd",
            "Uyghur": "uig",
            "Uzbek (Cyrillic)": "uzb_cyrl",
            "Uzbek": "uzb",
            "Vietnamese script": "Vietnamese",
            "Vietnamese": "vie",
            "Welsh": "cym",
            "Yiddish": "yid",
            "Yoruba": "yor",
        }

        # Load settings
        self.settings = Settings(self)

    def display_banner(self):
        """
        Raw ASCII art example:
        ╭──────────────────────────╮
        │           ▄██▄           │
        │          ██████          │
        │         ███▀▀▀██         │
        │        ███   ████        │
        │       ███   ██████       │
        │      ███   ▀▀▀▀████      │
        │     ███████  ▄██████     │
        │    ███████ ▄█████████    │
        │   ████████████████████   │
        │    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    │
        │                          │
        │    Dangerzone v0.1.5     │
        │ https://dangerzone.rocks │
        ╰──────────────────────────╯
        """

        print(Back.BLACK + Fore.YELLOW + Style.DIM + "╭──────────────────────────╮")
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "           ▄██▄           "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "          ██████          "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "         ███▀▀▀██         "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "        ███   ████        "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "       ███   ██████       "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "      ███   ▀▀▀▀████      "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "     ███████  ▄██████     "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "    ███████ ▄█████████    "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "   ████████████████████   "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Fore.LIGHTYELLOW_EX
            + Style.NORMAL
            + "    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(Back.BLACK + Fore.YELLOW + Style.DIM + "│                          │")
        left_spaces = (15 - len(self.version) - 1) // 2
        right_spaces = left_spaces
        if left_spaces + len(self.version) + 1 + right_spaces < 15:
            right_spaces += 1
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Style.RESET_ALL
            + Back.BLACK
            + Fore.LIGHTWHITE_EX
            + Style.BRIGHT
            + f"{' '*left_spaces}Dangerzone v{self.version}{' '*right_spaces}"
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(
            Back.BLACK
            + Fore.YELLOW
            + Style.DIM
            + "│"
            + Style.RESET_ALL
            + Back.BLACK
            + Fore.LIGHTWHITE_EX
            + " https://dangerzone.rocks "
            + Fore.YELLOW
            + Style.DIM
            + "│"
        )
        print(Back.BLACK + Fore.YELLOW + Style.DIM + "╰──────────────────────────╯")

    def get_container_runtime(self):
        if platform.system() == "Linux":
            return shutil.which("podman")
        else:
            return shutil.which("docker")

    def get_resource_path(self, filename):
        if getattr(sys, "dangerzone_dev", False):
            # Look for resources directory relative to python file
            prefix = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(inspect.getfile(inspect.currentframe()))
                    )
                ),
                "share",
            )
        else:
            if platform.system() == "Darwin":
                prefix = os.path.join(
                    os.path.dirname(os.path.dirname(sys.executable)), "Resources/share"
                )
            elif platform.system() == "Linux":
                prefix = os.path.join(sys.prefix, "share", "dangerzone")
            else:
                # Windows
                prefix = os.path.join(os.path.dirname(sys.executable), "share")

        resource_path = os.path.join(prefix, filename)
        return resource_path

    def get_subprocess_startupinfo(self):
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return startupinfo
        else:
            return None

    def install_container(self):
        """
        Make sure the podman container is installed. Linux only.
        """
        if self.is_container_installed():
            return

        # Load the container into podman
        print("Installing Dangerzone container image...")

        p = subprocess.Popen(
            [self.get_container_runtime(), "load"],
            stdin=subprocess.PIPE,
            startupinfo=self.get_subprocess_startupinfo(),
        )

        chunk_size = 10240
        compressed_container_path = self.get_resource_path("container.tar.gz")
        with gzip.open(compressed_container_path) as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) > 0:
                    p.stdin.write(chunk)
                else:
                    break
        p.communicate()

        if not self.is_container_installed():
            print("Failed to install the container image")
            return False

        print("Container image installed")
        return True

    def is_container_installed(self):
        """
        See if the podman container is installed. Linux only.
        """
        # Get the image id
        with open(self.get_resource_path("image-id.txt")) as f:
            expected_image_id = f.read().strip()

        # See if this image is already installed
        installed = False
        found_image_id = subprocess.check_output(
            [
                self.get_container_runtime(),
                "image",
                "list",
                "--format",
                "{{.ID}}",
                self.container_name,
            ],
            text=True,
            startupinfo=self.get_subprocess_startupinfo(),
        )
        found_image_id = found_image_id.strip()

        if found_image_id == expected_image_id:
            installed = True
        elif found_image_id == "":
            pass
        else:
            print("Deleting old dangerzone container image")

            try:
                subprocess.check_output(
                    [self.get_container_runtime(), "rmi", "--force", found_image_id],
                    startupinfo=self.get_subprocess_startupinfo(),
                )
            except:
                print("Couldn't delete old container image, so leaving it there")

        return installed
