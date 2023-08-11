# automates the process of solving reCAPTCHA challenges on web pages when using Selenium

## pip install solvacaptcha 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

```python

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

```