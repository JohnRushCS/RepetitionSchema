import random

class FlashCard(object):
    def __init__(self, word, definition, box_num):
        self.word = word
        self.definition = definition
        self.box = box_num

class LeitnerSpacing():
    def __init__(self, flash_cards):
        """
        @param flash_cards: (word, def) tuples or a dictionary of word def pairs
        @param num_boxes: number of groups
        """
        self.boxes = [[] for _ in range(5)]
        self.box_probs = [.5, .2, .15, .1, .05]
        for word, definition in self.flash_cards:
            fc = FlashCard(word, definition, 0)
            self.boxes[0].append(fc)
        self.results = 0
        self.cards_given = 0.0

    def _move_word(self, flash_card, new_box):
        box_num = flash_card.box
        if box_num == new_box:
            return
        for idx, fc in enumerate(self.boxes[box_num]):
            if fc is flash_card:
                self.boxes[box_num].pop(idx)
                break
        flash_card.box = new_box
        self.boxes[new_box].append(flash_card)

    def get_card(self):
        self.cards_given += 1
        rand_index = random.rand()
        running_sum = 0
        for idx in range(5):
            if rand_index <= running_sum + self.box_probs[idx]:
                box = idx
                break
        num_cards = len(self.boxes[box])
        card_idx = int(num_cards*random.rand())
        return self.boxes[box][card_idx]

    def report_result(self, flash_card, result):
        """
        @param word: the word to report results for
        @param result: the true or false value indicating whether
                       correct or incorrect.
        """
        self.results += int(result)
        if result:
            word_box = flash_card.box
            if word_box != 0:
                self._move_word(flash_card, word_box-1)
        else:
            self._move_word(flash_card, 0)

    def __str__(self):
        return [[fc.word for fc in self.boxes[idx]] for idx in range(5)]

    def __repr__(self):
        print(("Current stats:\nPercent Correct:" 
               " {:.2%}\nSounds played: {:d}").format(self.results/self.cards_given,
                                                       int(self.cards_given)))
        return [[fc.word for fc in self.boxes[idx]] for idx in range(5)]
