import nbtlib

class block:
    def __init__(self, blockid:str, tag:dict={}, nbt:dict={}) -> None:
        # judge args
        assert (type(blockid)==str), "TypeError: Expecting string type like blockid=\"minecraft:stone\""
        assert (type(tag)==dict), "TypeError: Expecting dictionary type like tag={\"facing\":\"up\"}"
        assert (type(nbt)==dict), "TypeError: Expecting dictionary type like nbt={\"CustomName\":nbtlib.String(\'{\"text\":\"test\"}\')}"
        # tolerance
        if blockid:
            if ":" not in blockid: blockid="minecraft:"+blockid
        # banned
        assert (blockid != "minecraft:air"), "AirBlockError: Air block is not allowed to create"
        # initialize
        self.blockid=blockid
        self.tag=tag
        self.nbt=nbt
    
    def same(block1, block2):
        '''
        judge whether two blocks are the same
        Inputs:
            block1, block2: block type
                the blocks that will be judged
        '''
        # judge args
        assert type(block2)==type(block1)==block, "TypeError: Expecting block type like block(\"minecraft:stone\")"
        # execute
        if block1.blockid==block2.blockid and block1.tag==block2.tag and block1.nbt==block2.nbt:    return True
        else:                                                                                       return False
    
    def copy(self):
        '''
        new a block
        no input
        '''
        return block(self.blockid, self.tag, self.nbt)

class pyschem:
    def __init__(self, offset:list=[0, 0, 0], weoffset:list=[0, 0, 0]):
        # judge arguments
        assert (type(offset)==list)
        # Initialize arguments
        self.offset=offset
        self.weoffset=weoffset
        self.content={}
    
    def size(self) -> tuple:
        '''
        size of the schematic
        no input
        '''
        x=y=z=0
        if self.content:
            for pos in self.content.keys():
                if pos[0]>x: x=pos[0]
                if pos[1]>y: y=pos[1]
                if pos[2]>z: z=pos[2]
            return (x+1, y+1, z+1)
        else:
            return (0, 0, 0)

    def setblock(self, *pos:tuple, repblock:block):
        '''
        set a block
        Inputs:
            pos: tuple with 3 integers that are not nagetive
                position of a block that will be set
        '''
        # judge arguments
        assert (type(pos)==tuple and len(pos)==3 and all(type(t)==int and t>=0 for t in pos)), "PositionError: Expecting tuple with 3 integers that are not negative"
        assert (type(repblock)==block), "TypeError: Expecting block type like repblock=\"minecraft:stone\""
        # set block
        self.content[pos]=repblock.copy()
    
    def delblock(self, *pos:tuple):
        '''
        delete a block
        Inputs:
            pos: tuple with 3 integers that are not nagetive
                position of a block that will be deleted
        '''
        assert (type(pos)==tuple and len(pos)==3 and all(t>=0 and type(t)==int for t in pos)), "PositionError: Expecting tuple with 3 integers that are not negative"
        if pos in self.content.keys():
            del self.content[pos]

    def fill(self, repblock:block, pos1:tuple, pos2:tuple=None, mode:str="destroy"):
        '''
        fill certain area with certain block
        Inputs:
            repblock: block type
                block that will be filled with
            pos1, pos2: tuple with 3 integers that are not nagetive
                selection position, pos2 should be at x+ y+ z+ dircetion of pos1
                if pos2 == None, selection is from pos1 to the farthest position
                pos2 default value: None
        '''
        # judge arguments
        assert (type(repblock==block)), "TypeError: Expecting block type like repblock=\"minecraft:stone\""
        assert ((len(pos1)==3 and all(t>=0 and type(t)==int for t in pos1)) and type(pos1)==tuple), "PositionError: Expecting tuple with 3 integers that are not negative"
        if not pos2:
            assert ((len(pos2)==3 and all(t>=0 and type(t)==int for t in pos2)) and type(pos2)==tuple), "PositionError: Expecting tuple with 3 integers that are not negative"
        assert (mode in ("destroy", "replace")), "ModeError: Unknown mode, expecting \"destroy\" or \"replace\""
        # fill blocks
        for x in range(pos1[0], pos2[0]+1):
            for y in range(pos1[1], pos2[1]+1):
                for z in range(pos1[2], pos2[2]+1):
                    if mode=="replace":
                        self.setblock(x, y, z, repblock.copy())
                    else:
                        if (x, y, z) not in self.content.keys():
                            self.setblock(x, y, z, repblock.copy())

    def count(self) -> int:
        '''
        count how many blocks are there in the schematic
        '''
        return len(self.content)

    def remove(self, pos1:tuple=None, pos2:tuple=None, isblock:block=None):
        '''
        remove all blocks in certain area
        Inputs:
            pos1, pos2: tuple with 3 integers that are not nagetive
                selection position, pos2 should be at x+ y+ z+ dircetion of pos1
                if input == None, selection is the whole schematic
                default value: None
            isblock: block type
                only remove target block if isblock is not None
        '''
        # judge arguments
        assert (type(isblock)==block or isblock==None), "TypeError: Expecting block type like block(\"minecraft:stone\")"
        if pos1:
            # judge arguments
            assert (type(pos1)==tuple and len(pos1)==3 and all(t>0 for t in pos1)), "PositionError: Expecting tuple with 3 integers that are not nagetive"
            assert (pos1[0]<=pos2[0] and pos1[1]<=pos2[1] and pos1[2]<=pos2[2]), "SelectionError: Expecting pos2 has 3 integers all bigger than that in pos1"
            # execute
            if pos2:
                assert (type(pos2)==tuple and len(pos2)==3 and all(t>0 for t in pos2)), "PositionError: Expecting tuple with 3 integers that are not nagetive"
            else:
                pos2=(self.size()[0]-1, self.size()[0]-1, self.size()[0]-1)
            for x in range(pos1[0], pos2[0]+1):
                for y in range(pos1[1], pos2[1]+1):
                    for z in range(pos1[2], pos2[2]+1):
                        if (x, y, z) in self.content.keys():
                            if isblock:
                                assert (type(isblock)==block), "TypeError: Expecting block type"
                                if block.same(isblock, self.content[x, y, z]):
                                    self.delblock(x, y, z)
                            else:
                                self.delblock(x, y, z)
        else:
            if isblock:
                for tmppos in self.content.keys():
                    if block.same(self.content[tmppos], isblock):
                        self.delblock(tmppos)
            else:
                self.content={}

    def place(self, schem, *pos:tuple, mode:str="replace", clear:bool=True):
        '''
        place a schematic at target position
        Inputs:
            schem: pyschem type
                schematic that will be placed
            pos: tuple with 3 integers that are not nagative
                target position that schem is going to be placed
            mode: string type in ("replace", "destroy")
                "replace": the position with block will not be replaced
                "destroy": the position with block will be replaced
                default value: "replace"
            clear: boolean type
                whether the target area will be cleared before place the selection
        '''
        # judge args
        assert (type(schem)==pyschem), "Invalid schem! Expecting pyschem type"
        assert (type(pos)==tuple and all(type(t)==int for t in pos) and len(pos)==3), "TypeError Expecting tuple with 3 integers that are not nagetive"
        assert (mode in ("replace", "destroy")), "ModeError, Unknown mode, expecting \"replace\" or mode=\"destroy\""
        assert (type(clear)==bool), "TypeError: Expecting bool type"
        # clear blocks if true
        if clear: self.remove(pos1=pos, pos2=(pos[0]+schem.size()[0], pos[1]+schem.size()[1], pos[2]+schem.size()[2]))
        # execute
        for tmppos in schem.content.keys():
            if mode=="replace":
                if (tmppos[0]+pos[0], tmppos[1]+pos[1], tmppos[2]+pos[2]) not in self.content.keys():
                    self.setblock(tmppos[0]+pos[0], tmppos[1]+pos[1], tmppos[2]+pos[2], repblock=schem.content[pos].copy())
            else:
                self.setblock(tmppos[0]+pos[0], tmppos[1]+pos[1], tmppos[2]+pos[2], repblock=schem.content[pos].copy())

    def copy(self, pos2:tuple=None, pos1:tuple=(0, 0, 0), reserve:bool=True):
        '''
        new a schematic
        Inputs:
            pos1, pos2: tuple with 3 integers that are not nagetive
                selection position, pos2 should be at x+ y+ z+ dircetion of pos1
            reserve: boolean type
                whether the selection will be removed
                default value: False
        '''
        assert (type(reserve)==bool), "TypeError: Expecting boolean type"
        if pos2:
            # judge args
            assert (type(pos1)==tuple and len(pos1)==3 and all(t>0 for t in pos1)) and (type(pos2)==tuple and len(pos2)==3 and all(t>0 for t in pos2)), "Invalid position! Expecting tuple with 3 positive integers"
            assert (pos1[0]<=pos2[0] and pos1[1]<=pos2[1] and pos1[2]<=pos2[2]), "SelectionError: Expecting pos2 has 3 integers all bigger than that in pos1"
            # judge size
            assert (pos2[0]<self.size()[0] and pos2[1]<self.size()[1] and pos2[2]<self.size()[2]), "SelectionError: Reach out of the temp schematic"
            # execute
            output=pyschem()
            for x in range(pos1[0], pos2[0]+1):
                for y in range(pos1[1], pos2[1]+1):
                    for z in range(pos1[2], pos2[2]+1):
                        if (x, y, z) in self.content.keys():
                            output.setblock(x, y, z, repblock=self.content[x, y, z].copy())
                            if not reserve:
                                self.delblock(x, y, z)
        else:
            output=pyschem()
            output.content=self.content.copy()
            output.offset=self.offset.copy()
            output.weoffset=self.weoffset.copy()
            if not reserve:
                self.remove()
        return output

    def clone(self, *target:tuple, pos1:tuple=None, pos2:tuple=None, reserve:bool=True, mode:str="replace", clear:bool=True):
        '''
        clone an selection to target position
        Inputs:
            target: tuple with 3 integers that are not nagetive
                the position that a selection is going to place
                No default value
            pos1, pos2: tuple with 3 integers that are not nagetive
                selection position, pos2 should be at x+ y+ z+ dircetion of pos1
                if input == None, selection is the whole schematic
                default value: None
            reserve: boolean type
                whether the selection will be removed
                default value: True
            mode: string type in ("replace", "destroy")
                "replace": the position with block will not be replaced
                "destroy": the position with block will be replaced
                default value: "replace"
            clear: boolean type
                whether the target area will be cleared before place the selection
        '''
        # judge args
        assert (all(type(t)==int and t>=0 for t in target)), "TypeErrpr: Expecting tuple type with 3 integers that are not negative"
        assert (type(reserve)==bool), "TypeError: Expecting bool type"
        assert (mode in ("replace", "destroy")), "ModeError: Unknown mode, expecting \"destroy\" or \"replace\""
        assert (type(clear)==bool), "TypeError: Expecting bool type"
        # generate new schem
        if pos1:
            # judge args
            assert (type(pos1)==tuple and all(type(t)==int and t>=0 for t in pos1)) and (type(pos2)==tuple and all(type(t)==int and t>=0 for t in pos2)), "TypeErrpr: Expecting tuple with 3 integers that are not negative"
            # judge position
            assert (pos1[0]<=pos2[0] and pos1[1]<=pos2[1] and pos1[2]<=pos2[2]), "SelectionError: Expecting pos2 has 3 integers all bigger than that in pos1"
            
            #execute
            # generate temp schematic
            tmp=self.copy(pos1=pos1, pos2=(pos2[0]+1, pos2[1]+1, pos2[2]+1))
            # clear if true
            if not reserve:
                self.remove(pos1=pos1, pos2=(pos2[0]+1, pos2[1]+1, pos2[2]+1))
        else:
            tmp=self.copy()
            # clear if true
            if not reserve:
                self.remove()
        # place schematic
        self.place(self, pos=target, mode=mode, clear=clear)
        del tmp

    def dump(self, loc:str=None):
        '''
        dump pyschem to schem file
        Inputs:
            loc: string type
                the location of the file
        '''
        # start transform
        palettes={}
        palette=0
        blockdatas=[]
        blockentities=[]
        for y in range(self.size()[1]):
            for z in range(self.size()[2]):
                for x in range(self.size()[0]):
                    # get block name
                    blockname=self.content[x, y, z].blockid
                    if self.content[x, y, z].tag:
                        blockname+="["
                        for tagName in self.content[x, y, z].tag.keys():
                            blockname+=tagName+"="+self.content[x, y, z].tag[tagName]+","
                        blockname[-1]="]"
                    # get block entities if own
                    if self.content[x, y, z].nbt:
                        blockentity=self.content[x, y, z].nbt
                        blockentity["Pos"]=nbtlib.IntArray((x, y, z))
                    # record palette
                    if blockname not in palettes.keys():
                        palettes[blockname]=nbtlib.Int(palette)
                        palette+=1
                    # record blockdata
                    blockdatas.append(nbtlib.Int(palettes[blockname]))
                    # record block entity
                    if self.content[x, y, z].nbt:
                        blockentities.append(blockentity)
        # initialize
        tmp=nbtlib.File({
            "": nbtlib.Compound({
                "Width": nbtlib.Short(self.size()[0]),
                "Height": nbtlib.Short(self.size()[1]),
                "Length": nbtlib.Short(self.size()[2]),
                "Offset": nbtlib.IntArray(self.offset),
                "BlockEntities": nbtlib.List[nbtlib.Compound](blockentities),
                "Palette": nbtlib.Compound(palettes),
                "BlockData": nbtlib.ByteArray(blockdatas),
                "Metadata": nbtlib.Compound({
                    "WEOffsetX": nbtlib.Int(self.weoffset[0]),
                    "WEOffsetY": nbtlib.Int(self.weoffset[1]),
                    "WEOffsetZ": nbtlib.Int(self.weoffset[2])
                }),
                "Version": nbtlib.Int(2),
                "DataVersion": nbtlib.Int(2586),
                "PaletteMax": nbtlib.Int(len(palettes))
            })
        })
        # save file
        tmp.save(loc, gzipped=True)