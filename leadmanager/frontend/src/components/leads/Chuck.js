import React, { useState, useEffect } from 'react'

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
        // var sound = new Audio("upper-cut.mp3")
        // sound.play()
      }
    
      useEffect(() => {
        fetch("https://chuck-norris-quote-generator.herokuapp.com/jokes")
          .then(data => data.json())
          .then(JSONdata => {
            console.log("Chuck Data", JSONdata)
            setJokes(JSONdata.data.jokes)
          })
      }, [])

    return (
        <div>
            <h1 onClick={() => generateQuote()}>Chuck Norris</h1>
        </div>
    )
}
