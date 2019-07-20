BOS = 'xxbos'
PAD = 'xxpad'
EOS = 'xxeos'
S2SCLS = 'xxs2scls' # used for sequence2sequence start of translation
MASK = 'xxmask'
CSEQ = 'xxcseq'
MSEQ = 'xxmseq'
NSCLS = 'xxnscls'

SEP = 'xxsep' # separator idx = -1 (part of notes)

SPECIAL_TOKS = [BOS, PAD, EOS, S2SCLS, MASK, CSEQ, MSEQ, NSCLS, SEP] # Important: SEP token must be last

NOTE_TOKS = [f'n{i}' for i in range(NOTE_SIZE)] 
DUR_TOKS = [f'd{i}' for i in range(DUR_SIZE)]
NOTE_START, NOTE_END = NOTE_TOKS[0], NOTE_TOKS[-1]
DUR_START, DUR_END = DUR_TOKS[0], DUR_TOKS[-1]

MTEMPO_SIZE = 10
MTEMPO_OFF = 'mt0'
MTEMPO_TOKS = [f'mt{i}' for i in range(MTEMPO_SIZE)]

# Vocab - token to index mapping
class MusicVocab():
    "Contain the correspondence between numbers and tokens and numericalize."
    def __init__(self, itos:Collection[str]):
        self.itos = itos
        self.stoi = {v:k for k,v in enumerate(self.itos)}

    def numericalize(self, t:Collection[str]) -> List[int]:
        "Convert a list of tokens `t` to their ids."
        return [self.stoi[w] for w in t]

    def textify(self, nums:Collection[int], sep=' ') -> List[str]:
        "Convert a list of `nums` to their tokens."
        return sep.join([self.itos[i] for i in nums]) if sep is not None else [self.itos[i] for i in nums]
    @property 
    def mask_idx(self): return self.stoi[MASK]
    @property 
    def pad_idx(self): return self.stoi[PAD]
    @property
    def bos_idx(self): return self.stoi[BOS]
    @property
    def sep_idx(self): return self.stoi[SEP]
    @property
    def npenc_range(self): return (vocab.stoi[SEP], vocab.stoi[DUR_END]+1)
    @property
    def note_range(self): return vocab.stoi[NOTE_START], vocab.stoi[NOTE_END]+1
    @property
    def dur_range(self): return vocab.stoi[DUR_START], vocab.stoi[DUR_END]+1

    def is_duration(self, idx): 
        return idx >= self.dur_range[0] and idx < self.dur_range[1]
        
    def __getstate__(self):
        return {'itos':self.itos}

    def __setstate__(self, state:dict):
        self.itos = state['itos']
        self.stoi = {v:k for k,v in enumerate(self.itos)}

    def save(self, path):
        "Save `self.itos` in `path`"
        pickle.dump(self.itos, open(path, 'wb'))

    @classmethod
    def create(cls) -> 'Vocab':
        "Create a vocabulary from a set of `tokens`."
        itos = SPECIAL_TOKS + NOTE_TOKS + DUR_TOKS + MTEMPO_TOKS
        if len(itos)%8 != 0:
            itos = itos + [f'dummy{i}' for i in range(len(itos)%8)]
        return cls(itos)
    
    @classmethod
    def load(cls, path):
        "Load the `Vocab` contained in `path`"
        itos = pickle.load(open(path, 'rb'))
        return cls(itos)
