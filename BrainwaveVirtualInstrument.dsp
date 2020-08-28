declare options "[osc:on]";
import("stdfaust.lib");

nChans = 8;
master = vslider("master",1,0,12,0.01): si.smoo;
start = checkbox("start"): si.smoo  ;
//pan = hslider("pan",0,0,1,0.01);

fm(carrierFreq, modFreq, ratio, index, gain, start, decay, rate, pan) = (os.osc(carrierFreq+os.osc(modFreq*ratio)*index)* en.arfe(0.1, decay, 0, os.lf_imptrain(rate)) * start * gain <:  _*(1-pan), _*pan)  ;
fmSynth(N) = hgroup("Synth",par(i,N,oneChan(i)))
with {
  oneChan(j) = vgroup("[%j]Channel %a", fm(carrierFreq, modFreq, ratio, index, gain, start, decay, rate, pan))
  with {
		a = j+1; // just so that band numbers don't start at 0
       	carrierFreq = vslider("[1]freq[style:knob]",20+(40*(((a / 2)+0.5):int)),60,4000,0.1): si.smoo; //default,min, max, step
		modFreq = vslider("[2]modFreq[style:knob]",20+(40*(((a / 2)+0.5):int)),60,4000,0.1): si.smoo;
		index = vslider("[3]index[style:knob]",100,20,20000,0.1): si.smoo;
		ratio = vslider("[4]ratio[style:knob]",0.01,0,1,0.01): si.smoo;
		decay = vslider("[5]decay[style:knob]",0.1,0.1,1,0.01): si.smoo;
		rate = vslider("[6]rate[style:knob]",1,1,16,1): si.smoo;
		pan = vslider("[7]pan[style:knob]",0.25+(0.5*(a % 2)),0,1,0.1);
		gain = vslider("[8]gain",1,0,12,0.01): si.smoo;
		start = checkbox("[9]start"): si.smoo;
    };
};


process = hgroup("All", fmSynth(nChans) :> _,_ : vgroup("[99]", dm.freeverb_demo :>_*master*start,_*master*start));  


// :// 