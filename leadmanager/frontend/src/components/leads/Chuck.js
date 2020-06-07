import React, { useState, useEffect } from 'react';
import chuck from "./chuck-norris.png";

// import html from './file.html';

export default function Chuck() {
  const [jokes, setJokes] = useState([])
  const [currentJoke, setCurrentJoke] = useState([])
  const [tag, setTag] = useState([])

  // axios
  // .get("/api/leads/")

  const getRandomInt = (max) => {
    let min = 0
    return Math.floor(Math.random() * (max - min)) + min;
  }

  const generateQuote = () => {
    const randomIndex = getRandomInt(jokes.length)
    console.log("randomIndex", randomIndex)
    const randomJoke = jokes[randomIndex]
    console.log("randomJoke", randomJoke)

    setCurrentJoke(randomJoke.joke)
    setTag(randomJoke.categories)
    var sound = new Audio("upper-cut.mp3")
    sound.play()
    console.log("this LOADED143")
  }

  useEffect(() => {
    console.log("this LOADED143")
    fetch("https://chuck-norris-quote-generator.herokuapp.com/jokes")
      .then(data => data.json())
      .then(JSONdata => {
        console.log("Chuck Data", JSONdata)
        setJokes(JSONdata.data.jokes)
      })
  }, [])

  return (
    <div className="container">
      <div className="row justify-content-center py-5">
        <div className="col-8 text-center">
          <h1 onClick={() => generateQuote()}>Chuck Norris</h1>
          <img src={chuck} alt="chuck" style={{ height: "200px" }} />
          <h1 className="pb-2">Hello Chuck143!</h1>
          <p className="pb-2">An app for randomly generating Chuck Norris jokes.</p>
          <button className="btn btn-danger btn-lg" onClick={() => generateQuote()}>Karate Chop</button>
        </div>
      </div>
      <p className="row justify-content-center"> {currentJoke} </p>
    </div>
  )
}
