declare name "Brainwave Virtual Instrument"; 
declare version "1.0";
declare author "Nico Daleman"; 


declare options "[osc:on]";
declare options "[midi:on]";
import("stdfaust.lib");

nChans = 8;
master = vslider("master",0.5,0,1,0.01): si.smoo;
start = checkbox("start"): si.smoo  ;
//pan = hslider("pan",0,0,1,0.01);

fm(carrierFreq, modFreq, ratio, index, gain, start, decay, rate, pan) = (os.osc(carrierFreq+os.osc(modFreq*ratio)*index)* en.ar(0.01, decay / rate, os.lf_imptrain(rate)) * start * gain <:  _*(1-pan), _*pan)  ;
fmSynth(N) = hgroup("Synth",par(i,N,oneChan(i)))
with {
  oneChan(j) = vgroup("[%j]Channel %a", fm(carrierFreq, modFreq, ratio, index, gain, start, decay, rate, pan))
  with {
		a = j+1; // just so that band numbers don't start at 0
		s = j + 77;// sliders
		k = j + 13;// knob1
		l = j + 29;// knob2
		m = j + 49;// knob3
       	carrierFreq = nentry("[1]freq",20+(40*(((a / 2)+0.5):int)),60,4000,0.1): si.smoo; //default,min, max, step
		modFreq = nentry("[2]modFreq",20+(40*(((a / 2)+0.5):int)),60,4000,0.1): si.smoo;
		index = vslider("[3]index[style:knob][midi:ctrl %k][scale:log]",100,20,20000,0.1): si.smoo;
		ratio = vslider("[4]ratio[style:knob][midi:ctrl %l]",0.01,0,1,0.01): si.smoo;
		decay = vslider("[5]decay[style:knob][midi:ctrl %m]",0.1,0.1,1,0.01): si.smoo;
		rate = nentry("[6]rate",a / 2+0.5:int,1,16,1): si.smoo;
		pan = nentry("[7]pan",0.25+(0.5*(a % 2)),0,1,0.1);
		gain = vslider("[8]gain[midi:ctrl %s]",0.5,0,1,0.01): si.smoo;
		start = checkbox("[9]start"): si.smoo;
    };
};


process = hgroup("[1]", fmSynth(nChans) :> _,_ : vgroup("[99]", dm.freeverb_demo :>_*master*start,_*master*start));  


// :// 