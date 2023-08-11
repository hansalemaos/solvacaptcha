import os
import re
import tempfile
import time
from ffmpegaudiorecord import start_recording
from audiotranser import transcribe_audio
from kthread_sleep import sleep
from touchtouch import touch

from a_selenium_iframes_crawler import Iframes

import kthread


def solva_captcha(
    driver,
    expected_conditions,
    WebDriverWait,
    By,
    ffmpegexe,
    sleep_after_recording_started=10,
    sleep_after_each_click=10,
    captchatitle="""[title="reCAPTCHA"]""",
    language="en",
    cpus=5,
    blas=True,
    audiodevice=0,
    silent_seconds_stop=3,
    silence_threshold=-25,
    selector=(
        ("button", "audio", "outerHTML"),
        ("button", ">PLAY<", "outerHTML"),
        ("input", 'id="audio-response"', "outerHTML"),
        ("button", ">Verify<", "outerHTML"),
    ),
):
    r"""
    solva_captcha - Automated CAPTCHA Solver

    This function automates the process of solving reCAPTCHA challenges on web pages.
    It uses audio-based CAPTCHA challenges as an example and employs audio recording,
    transcription, and interaction with web elements to solve the challenge.
    It is recommended to install: Virtual Audio Cable (VAC) - the free version is more than enough
    https://vac.muzychenko.net/en/download.htm

    Parameters:
        driver: WebDriver
            The Selenium WebDriver instance.
        expected_conditions: module
            The module containing expected conditions for WebDriver waits.
        WebDriverWait: class
            The class for setting up explicit waits with WebDriver.
        By: class
            The class for locating elements with WebDriver.
        ffmpegexe: str
            The path to the FFmpeg executable for audio processing.
        sleep_after_recording_started: int, optional
            Time to sleep (in seconds) after audio recording starts.
        sleep_after_each_click: int, optional
            Time to sleep (in seconds) after each interaction/click.
        captchatitle: str, optional
            The CSS selector for identifying the CAPTCHA challenge element.
        language: str, optional
            The spoken language for audio transcription.
        cpus: int, optional
            Number of CPU cores to use during audio processing.
        blas: bool, optional
            Whether to use BLAS acceleration for audio processing.
        audiodevice: int, optional
            Index of the audio device for recording.
        silent_seconds_stop: int, optional
            Duration of silence to stop audio recording (in seconds).
        silence_threshold: int, optional
            Threshold for silence detection during audio recording.
        selector: tuple of tuples, optional
            CSS selectors for identifying various CAPTCHA interaction elements.

    Returns:
        None

    Note:
        This function automates solving a specific type of audio-based reCAPTCHA challenge. It records audio,
        transcribes it to text, interacts with the CAPTCHA elements, and submits the solution.

    Example:
        from selenium.webdriver.support import expected_conditions
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.common.by import By
        from operagxdriver import start_opera_driver

        from solvacaptcha import solva_captcha

        driver = start_opera_driver(
            opera_browser_exe=r"C:\Program Files\Opera GX\opera.exe",
            opera_driver_exe=r"C:\ProgramData\anaconda3\envs\dfdir\operadriver.exe",
            userdir="c:\\operabrowserprofile2",
            arguments=(
                "--no-sandbox",
                "--test-type",
                "--no-default-browser-check",
                "--no-first-run",
                "--incognito",
                "--start-maximized",
            ),
        )
        driver.get("https://www.google.com/recaptcha/api2/demo")

        solva_captcha(
            driver,
            expected_conditions,
            WebDriverWait,
            By,
            ffmpegexe=r"C:\ffmpeg\ffmpeg.exe",
            sleep_after_recording_started=10,
            sleep_after_each_click=10,
            captchatitle='[title="reCAPTCHA"]',
            language="en",
            cpus=5,
            blas=True,
            audiodevice=0,
            silent_seconds_stop=3,
            silence_threshold=-30,
            selector=(
                ("button", "audio", "outerHTML"),
                ("button", ">PLAY<", "outerHTML"),
                ("input", 'id="audio-response"', "outerHTML"),
                ("button", ">Verify<", "outerHTML"),
            ),
        )

    """

    isdone = False

    def record_audio(audiofile, ffmpegexe=ffmpegexe):
        nonlocal isdone
        print(
            "if you don't know the index of your device, pass audiodevice=10000000 That will raise an Exception and will show you all devices"
        )
        audio_data = start_recording(
            ffmpegexe=ffmpegexe,
            audiodevice=audiodevice,
            silent_seconds_stop=silent_seconds_stop,
            silence_threshold=silence_threshold,
        )
        audio_data.export(audiofile)
        isdone = True

    def get_wav_tmp():
        suffix = ".wav"
        tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        filename = tfp.name
        filename = os.path.normpath(filename)
        tfp.close()
        touch(filename)
        return filename

    def get_text_from_audio(audiofile):
        dftext = transcribe_audio(
            inputfile=audiofile,
            small_large="large",
            blas=blas,
            silence_threshold=-30,  # ignored if == 0 or None
            min_silence_len=500,  # ignored if silence_threshold == 0 or None
            keep_silence=1000,  # ignored if silence_threshold == 0 or None
            threads=cpus,  # number of threads to use during computation
            processors=1,  # number of processors to use during computation
            offset_t=0,  # time offset in milliseconds
            offset_n=0,  # segment index offset
            duration=0,  # duration of audio to process in milliseconds
            max_context=-1,  # maximum number of text context tokens to store
            max_len=0,  # maximum segment length in characters
            best_of=2,  # number of best candidates to keep
            beam_size=-1,  # beam size for beam search
            word_thold=0.01,  # word timestamp probability threshold
            entropy_thold=2.40,  # entropy threshold for decoder fail
            logprob_thold=-1.00,  # log probability threshold for decoder fail
            speed_up=False,  # speed up audio by x2 (reduced accuracy)
            translate=False,  # translate from source language to english
            diarize=False,  # stereo audio diarization
            language=language,  # spoken language ('auto' for auto_detect)
        )
        texttowrite = " ".join(
            dftext.drop_duplicates(subset="text").text.str.strip().to_list()
        )
        texttowrite = re.sub(r"[^\w\s]+", " ", texttowrite)
        texttowrite = re.sub(r"\s+", " ", texttowrite).strip()
        return texttowrite

    getiframes = lambda: Iframes(
        driver,
        By,
        WebDriverWait,
        expected_conditions,
        seperator_for_duplicated_iframe="Ç",
        ignore_google_ads=True,
    )
    didweclick = False
    while not didweclick:
        driver.switch_to.default_content()
        iframes = getiframes()
        for ini, iframe in enumerate(iframes.iframes):
            try:
                if captchatitle not in iframe:
                    continue
                iframes.switch_to(iframe)
                elemethods = driver.find_elements(By.CSS_SELECTOR, "span")
                for ele in elemethods:
                    try:
                        ele.location_once_scrolled_into_view
                        ele.click()
                        didweclick = True
                        break
                    except Exception:
                        continue

                if didweclick:
                    break
            except Exception as fe:
                continue

    didweclick = False
    while not didweclick:
        iframes = getiframes()
        for ini, iframe in enumerate(iframes.iframes):
            try:
                if captchatitle not in iframe:
                    continue
                iframes.switch_to(iframe)
                elemethods = driver.find_elements(By.CSS_SELECTOR, selector[0][0])
                for ele in elemethods:
                    try:
                        if selector[0][1] in (ele.get_attribute(selector[0][2])):
                            try:
                                ele.location_once_scrolled_into_view
                                ele.click()
                                didweclick = True
                                break
                            except Exception:
                                continue
                    except Exception:
                        pass
                if didweclick:
                    break
            except Exception as fe:
                continue

    audiofile = get_wav_tmp()
    thre = kthread.KThread(
        target=record_audio,
        name="pro",
        args=(audiofile,),
        kwargs={"ffmpegexe": ffmpegexe},
    )
    thre.start()
    time.sleep(sleep_after_recording_started)
    while not isdone:
        iframes = getiframes()
        for ini, iframe in enumerate(iframes.iframes):
            try:
                if captchatitle not in iframe:
                    continue
                iframes.switch_to(iframe)
                elemethods = driver.find_elements(By.CSS_SELECTOR, selector[1][0])
                for ele in elemethods:
                    try:
                        if selector[1][1] in (ele.get_attribute(selector[1][2])):
                            try:
                                ele.location_once_scrolled_into_view
                                ele.click()
                                sleep(sleep_after_each_click)
                                if isdone:
                                    break
                            except Exception:
                                continue
                    except Exception:
                        pass
                if isdone:
                    break
            except Exception as fe:
                continue

    texttowrite = get_text_from_audio(audiofile)

    didweclick = False
    while not didweclick:
        iframes = getiframes()
        for ini, iframe in enumerate(iframes.iframes):
            try:
                if captchatitle not in iframe:
                    continue
                iframes.switch_to(iframe)
                elemethods = driver.find_elements(By.CSS_SELECTOR, selector[2][0])

                for ele in elemethods:
                    try:
                        if selector[2][1] in (ele.get_attribute(selector[2][2])):
                            try:
                                ele.send_keys(texttowrite)
                                didweclick = True
                                break
                            except Exception:
                                continue
                    except Exception:
                        pass
                if didweclick:
                    break
            except Exception as fe:
                continue

    didweclick = False
    while not didweclick:
        iframes = getiframes()
        for ini, iframe in enumerate(iframes.iframes):
            try:
                if captchatitle not in iframe:
                    continue
                iframes.switch_to(iframe)
                elemethods = driver.find_elements(By.CSS_SELECTOR, selector[3][0])
                for ele in elemethods:
                    try:
                        if selector[3][1] in (ele.get_attribute(selector[3][2])):
                            try:
                                ele.click()
                                didweclick = True
                                break
                            except Exception:
                                continue
                    except Exception:
                        pass
                if didweclick:
                    break
            except Exception as fe:
                continue
