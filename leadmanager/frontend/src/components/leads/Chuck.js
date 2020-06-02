import React, { useState, useEffect } from 'react'

export default function Chuck() {

    const [jokes, setJokes] = useState([])

    // axios
    // .get("/api/leads/")

    const getRandomInt = (max) => {
        let min = 0
        return Math.floor(Math.random() * (max - min)) + min;
      }
    
    const generateQuote = () => {
        const randomIndex = this.getRandomInt(this.state.jokes.length)
        const randomJoke = this.state.jokes[randomIndex]
        this.setState({
          quote: randomJoke.joke,
          tags: randomJoke.categories
        })
        var sound = new Audio("upper-cut.mp3")
        sound.play()
      }
    
      useEffect(() => {
        fetch("https://chuck-norris-quote-generator.herokuapp.com/jokes")
          .then(data => data.json())
          .then(JSONdata => {
            console.log(JSONdata)
            this.setState({ jokes: JSONdata.data.jokes })
          })
      }, [])

    return (
        <div>
            <h1>Chuck Norris</h1>
        </div>
    )
}
