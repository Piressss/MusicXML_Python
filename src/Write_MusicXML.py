#!/usr/bin/python
# -*- coding: utf-8 -*-

# Debug do fpga.bin

import os, sys, getopt, time, struct, re
import xml.etree.ElementTree as ET

# Classe para escrita do MusicXML

class WriteMusicXML:
    
    # Construtor
    def __init__(self, composer, title, instrument, division, clef, line, fifth, beats, beat_type):
        self.composer   = composer
        self.title      = title
        self.instrument = instrument
        self.division   = division
        self.clef       = clef
        self.line       = line
        self.fifth      = fifth
        self.beats      = beats
        self.beat_type  = beat_type
        self.score      =  ET.Element('score-partwise version')

    def WriteHeader(self):
         data = "\"<\?xml version=\"1.0\" encoding=\"UTF-16\" standalone=\"no\"?>\n"
         data = data + "\"<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 1.1 Partwise//EN\"\n"
         data = data + "\"http://www.musicxml.org/dtds/partwise.dtd\">\n"
         return data

    def WriteConfig(self):
        self.score.set('version','1.1')
        # SubElement 1 
        identification  = ET.SubElement(self.score,'identification')
        # SubElement 1.1
        creator = ET.SubElement(identification,'creator')
        creator.set('type',"composer")
        creator.text = self.composer
        # SubElement 1.2
        enconding = ET.SubElement(identification,'enconding')
        software  = ET.SubElement(enconding,'software')
        software.text = 'Encore'
        
        # SubElement 2
        defaults  = ET.SubElement(self.score,'defaults')
        # SubElement 2.1
        scaling  = ET.SubElement(defaults,'scaling')
        # SubElement 2.1.1
        millimeters = ET.SubElement(scaling,'millimeters')
        millimeters.text = '6.35'
        # SubElement 2.1.2
        tenths = ET.SubElement(scaling,'tenths')
        tenths.text = '40'

        # SubElement 3
        credit = ET.SubElement(self.score,'credit')
        # SubElement 3.1
        credit_words = ET.SubElement(credit,'credit-words')
        credit_words.set('justify','right')
        credit_words.set('valign','top')
        credit_words.text = self.composer

        # SubElement 4
        part_list = ET.SubElement(self.score,'part-list')
        # SubElement 4.1
        score_part = ET.SubElement(part_list,'score-part')
        score_part.set('id','P1')
        # SubElement 4.1.1
        part_name = ET.SubElement(score_part,'part-name')   
        # SubElement 4.1.2
        score_instrument = ET.SubElement(score_part,'score-instrument')
        score_instrument.set('id','P1-P2')
        # SubElement 4.1.2.1
        instrument_name = ET.SubElement(score_instrument,'instrument-name')
        instrument_name.text = self.instrument
        # SubElement 4.2.1
        midi_instrument = ET.SubElement(score_part,'midi-instrument')
        midi_instrument.set('id','P1-P2')
        # SubElement 4.2.1.1
        midi_channel = ET.SubElement(midi_instrument,'midi-channel')
        midi_channel.text = '1'

    def WriteMeasure(self,num,barline):
        if num == '1':
            # SubElement
            part = ET.SubElement(self.score,'part')
            part.set('id','P1')
            # SubElement
            measure = ET.SubElement(part,'measure')
            measure.set('number','1')
            # SubElement
            attributes = ET.SubElement(measure,'attributes')
            # SubElement
            divisions = ET.SubElement(attributes,'divisions')
            divisions.text = self.division
            # SubElement
            key = ET.SubElement(attributes,'key')
            # SubElement
            fifths = ET.SubElement(key,'fifths')
            fifths.text = self.fifth
            # SubElement
            time = ET.SubElement(attributes,'time')
            # SubElement
            beats = ET.SubElement(time,'beats')
            beats.text = self.beats
            # SubElement
            beat_type = ET.SubElement(time,'beat-type')
            beat_type.text = self.beat_type
            # SubElement
            staves = ET.SubElement(attributes,'staves')
            staves.text = '1'
            # SubElement
            clef = ET.SubElement(attributes,'clef')
            clef.set('number','1')
            # SubElement
            sign = ET.SubElement(clef,'sign')
            sign.text = self.clef
            # SubElement
            line = ET.SubElement(clef,'line')
            line.text = self.line
            # SubElement
            transpose = ET.SubElement(attributes,'transpose')
            # SubElement
            chromatic = ET.SubElement(transpose,'chromatic')
            chromatic.text = '0'
        else:
            # SubElement
            measure = ET.SubElement(self.score.find('part'),'measure')
            measure.set('number',num)
            # SubElement
            attributes = ET.SubElement(measure,'attributes')

    def WriteBar(self,location,barline_style,direction,barline_ending,ending_number):
        # SubElement
        barline = ET.SubElement(self.score.find('measure'),'barline')
        barline.set('location',location)
        # SubElement
        bar_style = ET.SubElement(barline,'bar-style')
        bar_style.text = (barline_style)
        if barline_ending != 'None':
            ending = ET.SubElement(barline,'ending')
            ending.set('type',barline_ending)
            ending.set('number',ending_number)
        # SubElement
        repeat = ET.SubElement(barline,'repeat')
        repeat.set('direction',direction)

    def WriteNote(note_name,note_octave,note_duration,note_type,note_accidental,note_stem,note_slur,slur_type,note_tied,tied_type,note_fermata,fermata_type):
        # Note Part
        note = ET.SubElement(self.score.find('measure'),'note')
        # SubElement
        pitch = ET.SubElement(note,'pitch')
        # SubElement
        step = ET.SubElement(pitch,'step')
        step.text = note_name
        # SubElement
        octave = ET.SubElement(pitch,'octave')
        octave.text = note_octave
        # SubElement
        duration = ET.SubElement(note,'duration')
        duration.text = note_duration 
        # SubElement
        voice = ET.SubElement(note,'voice')
        voice.text = '1'
        # SubElement
        type_s = ET.SubElement(note,'type')
        type_s.text = note_type
        # SubElement
        if note_accidental != 'none':
            accidental = ET.SubElement(note,'accidental')
            accidental.set('cautionary','no')
            accidental.text = note_accidental
        # SubElement
        stem = ET.SubElement(note,'stem')
        stem.text = note_stem
        # SubElement
        staff = ET.SubElement(note,'staff')
        staff.text = '1'
        # SubElement
        notations = ET.SubElement(note,'notations')
        if note_slur != 'None':
            slur = ET.SubElement(notations,'slur')
            slur.set('type',slur_type)
        if note_tied != 'None':
            tied = ET.SubElement(notations,'slur')
            tied.set('type',tied_type)
        if note_harmonic != 'None':
            technical = ET.SubElement(notations,'technical')
            # SubElement
            harmonic = ET.SubElement(technical,'harmonic')
            harmonic.set('placement','above')
        if note_fermata != 'None':
            fermata = ET.SubElement(notations,'fermata')
            fermata.set('type',fermata_type)

    def WriteDynamics(self,dynamics_name):
        # SubElement
        direction = ET.SubElement(self.score.find('measure'),'direction')
        direction.set('placement','above')
        # SubElement
        direction_type = ET.SubElement(direction,'direction-type')
        # SubElement
        dynamics = ET.SubElement(direction_type,'dynamics')
        # SubElement
        dynamics_type = ET.SubElement(direction_type,dynamics_name)
        # SubElement
        voice = ET.SubElement(direction,'voice')
        voice.text = ('1')
        # SubElement
        staff = ET.SubElement(direction,'staff')
        staff.text = ('1')
        
    def WriteRest(self,rest_duration,rest_type):
        # Note Part
        note = ET.SubElement(self.score.find('measure'),'note')
        # SubElement
        rest = ET.SubElement(note,'rest')
        # SubElement
        duration = ET.SubElement(rest,'duration')
        duration.text = (rest_duration)
        # SubElement
        voice = ET.SubElement(rest,'voice')
        voice.text = ('1')
        # SubElement
        type_r = ET.SubElement(rest,'type')
        type_r.text = (rest_type)
        # SubElement
        staff = ET.SubElement(rest,'staff')
        staff.text = ('1')


    
    def Indent(self):
        data = ET.tostring(self.score)
        data = re.sub('><','>\n<',data)
        data = data.split('\n') 

        inc   = '    '
        level = 0
        for i in range(len(data)):
            if re.search('/>', data[i]):
                data[i] = '\n' + (inc*level) + data[i]
                #level -= 1
            elif not re.search('</',data[i]):
                data[i] = '\n' + (inc*level) + data[i]
                level += 1
            else:
                if data[i][0:2] == '</':
                    level -= 1
                    data[i] = '\n' + (inc*level) + data[i]
                else:
                    data[i] = '\n' + (inc*level) + data[i]
             
        data = ''.join(data)

        return data
    
# TESTE
xml = Write_MusicXML("Felipe","None","Sax",'4','G','2','0','4','4')

myfile = open("teste.xml", "w")

data   = xml.Write_Header()
myfile.write(data)

xml.Write_Config()
xml.Write_Measure('1')
xml.Write_Measure('2')
data = xml.Indent()

#print xml.score.find('part')


myfile.write(data)

myfile.write("\n")
