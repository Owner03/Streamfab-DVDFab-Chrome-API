def get_license_challenge(self, session: Session) -> bytes:
        pssh = session.pssh
        if isinstance(pssh, Container):
            pssh = Box.build(pssh)
        if isinstance(pssh, bytes):
            pssh = base64.b64encode(pssh).decode()

        self.last_challenge = requests.post(
            url="https://www.deuhd.ru/v1/st/",
            data={
                "T": 1,
                "V": 3,
                "E": "trial user",
                "P": pssh,  # expects Base64
                "C": session.signed_device_certificate  # expects Base64
            }
        ).json()["FB"]

        challenge_2 = requests.post(
            url="https://drm-w-j2.dvdfab.cn/mk/",
            data={
                "T": 1,
                "A": 3,
                "E": "trial user",
                "K": "",
                "F": self.last_challenge  # expects Base64
            }
        ).json()["FB"]

        return base64.b64decode(challenge_2)

    def parse_license(self, session: Session, license_res: Union[bytes, str]) -> bool:
        if isinstance(license_res, bytes):
            license_res = base64.b64encode(license_res).decode()

        pssh = session.pssh
        if isinstance(pssh, Container):
            pssh = Box.build(pssh)
        if isinstance(pssh, bytes):
            pssh = base64.b64encode(pssh).decode()

        license_b64 = requests.post(
            url="https://drm-w-j2.dvdfab.cn/mk/",
            data={
                "T": 1,
                "A": 3,
                "E": "trial user",
                "K": "",
                "F": license_res  # expects Base64?
            }
        ).json()["FB"]

        keys = requests.post(
            url="https://www.deuhd.ru/v1/st/",
            data={
                "T": 2,
                "V": 3,
                "E": "trial user",
                "P": pssh,  # expects Base64
                "D": self.last_challenge,  # expects Base64
                "L": license_b64  # expects Base64
            }
        ).json()