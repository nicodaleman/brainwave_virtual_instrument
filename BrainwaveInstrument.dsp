declare options "[osc:on]";
import("stdfaust.lib");

nChans = 8;
master = vslider("master",1,0,12,0.01): si.smoo;
start = checkbox("start"): si.smoo  ;
//pan = sp.panner(0.5);
fm(carrierFreq, modFreq,  index, gain, start, decay, rate) = (os.osc(carrierFreq+os.osc(modFreq)*index)* en.arfe(0.1, decay, 0, os.lf_imptrain(rate)) * gain) * start;
fmSynth(N) = hgroup("Synth",par(i,N,oneChan(i))) //par or sum iteration (?)
with {
  oneChan(j) = vgroup("[%j]Channel %a", fm(carrierFreq, modFreq, index, gain, start, decay, rate))
  with {
		a = j+1; // just so that band numbers don't start at 0
       	carrierFreq = vslider("[1]freq[style:knob]",200*a,60,4000,0.1): si.smoo; //default,min, max, step
		modFreq = vslider("[2]modFreq[style:knob]",200*a,200,1600,0.1): si.smoo;
		index = vslider("[3]index[style:knob]",100,100,1000,0.1): si.smoo;
		decay = vslider("[4]decay[style:knob]",0.1,0.1,1,0.01): si.smoo;
		rate = vslider("[5]rate[style:knob]",1,1,16,1): si.smoo;
		//pan = sp.panner(vslider("[6]pan[style:knob]",0.125*a,0,1,0.1)) :> si.smoo;
		gain = vslider("[7]gain",0.3,0,1,0.01): si.smoo;
		start = checkbox("[8]start"): si.smoo;
    };
};


process = hgroup("All", fmSynth(nChans)) :> _,_; // :> _ * vgroup("masterCh", master * start)); // <: vgroup("[99]", dm.freeverb_demo)); 
	
	