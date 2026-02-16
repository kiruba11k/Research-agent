import React, { useState } from 'react';

import { Canvas } from '@react-three/fiber';

import { Sphere, MeshDistortMaterial } from '@react-three/drei';

import { motion, AnimatePresence } from 'framer-motion';

import { Search, Cpu, Loader2, FileText } from 'lucide-react';

import axios from 'axios';



const API_BASE =
"https://research-agent-n30i.onrender.com";



export default function App() {



  const [file, setFile] =
  useState(null);



  const [target, setTarget] =
  useState('');



  const [loading, setLoading] =
  useState(false);



  const [report, setReport] =
  useState(null);




  const runAnalysis = async () => {



    if(!target)

    {

      alert("Enter company");

      return;

    }



    setLoading(true);



    try {



      const formData =
      new FormData();



      formData.append(

        "target_company",

        target

      );



      if(file)

      {

        formData.append(

          "annual_report",

          file

        );

      }




      const res =
      await axios.post(

        `${API_BASE}/research`,

        formData,

        {

          headers:

          {

            "Content-Type":

            "multipart/form-data"

          }

        }

      );



      setReport(

        JSON.stringify(

          res.data,

          null,

          2

        )

      );



    }



    catch(e)

    {

      console.log(

        e.response?.data

      );



      alert(

        "Research failed"

      );

    }



    setLoading(false);



  };





  return (



<div className="min-h-screen bg-slate-950 text-slate-100 relative overflow-hidden">



<div className="absolute inset-0 opacity-30">

<Canvas>

<ambientLight />

<Sphere args={[1,100,200]} scale={2.5}>

<MeshDistortMaterial

color="#3b82f6"

speed={2}

distort={0.4}

/>

</Sphere>

</Canvas>

</div>





<div className="relative max-w-5xl mx-auto px-6 py-12">



<header className="text-center mb-16">



<motion.h1

initial={{y:-20}}

animate={{y:0}}

className="text-6xl font-black bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent"

>

DEEP RESEARCH AI

</motion.h1>



<p className="text-slate-400 mt-4">

Autonomous Account Orchestrator

</p>



</header>





<div className="grid grid-cols-1 lg:grid-cols-12 gap-10">





<div className="lg:col-span-4">



<div className="bg-slate-900/50 p-8 rounded-3xl">



<div className="flex gap-3 mb-8 text-blue-400">



<Search />



<h2>

Research Portal

</h2>



</div>





<input

value={target}

onChange={

e=>setTarget(

e.target.value

)

}

placeholder="Target Company"

className="w-full bg-slate-800 p-4 mb-4 rounded-xl"

/>





<input

type="file"

accept=".pdf"

onChange={

e=>setFile(

e.target.files[0]

)

}

className="w-full bg-slate-800 p-4 mb-4 rounded-xl"

/>





<button

onClick={runAnalysis}

disabled={loading}

className="w-full bg-blue-600 py-4 rounded-xl flex justify-center gap-2"

>



{

loading

?

<Loader2 className="animate-spin"/>

:

<Cpu/>

}



{

loading

?

"AGENTS WORKING"

:

"START ORCHESTRATION"

}



</button>



</div>



</div>







<div className="lg:col-span-8 min-h-[500px]">





<AnimatePresence>



{



report

?

<motion.div

initial={{opacity:0}}

animate={{opacity:1}}

className="bg-slate-900 p-8 rounded-3xl"

>



<div className="flex gap-2 mb-4">

<FileText/>

Generated Report

</div>



<pre className="whitespace-pre-wrap">

{report}

</pre>



</motion.div>



:

<div className="border border-white/10 rounded-3xl h-full flex items-center justify-center">

Awaiting Input Data

</div>



}



</AnimatePresence>





</div>





</div>





</div>





</div>



);



}
