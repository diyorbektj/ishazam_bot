from exceptions import NotFoundTrack


class Track:
    def __init__(self, music):
        self.music = music
        try:
            self.track = self.music['track']
            self.title = self.track['title']
            self.subtitle = self.track['subtitle']
            try:
                self.image = self.track['images']['coverarthq']
            except:
                self.image = 'image'
            try:
                self.test = self.track['sections'][-4]['text']
                self.text = '\n'.join([str(elem) for elem in self.test])
            except:
                try:
                    self.test = self.track['sections'][-3]['text']
                    self.text = '\n'.join([str(elem) for elem in self.test])
                except:
                    self.text = "test"
        except KeyError:
            raise NotFoundTrack

