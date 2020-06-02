import React from 'react'

export default function Chuck() {

    // axios
    // .get("/api/leads/")

    getRandomInt = (max) => {
        let min = 0
        return Math.floor(Math.random() * (max - min)) + min;
      }
    
      generateQuote = () => {
        const randomIndex = this.getRandomInt(this.state.jokes.length)
        const randomJoke = this.state.jokes[randomIndex]
        this.setState({
          quote: randomJoke.joke,
          tags: randomJoke.categories
        })
        var sound = new Audio("upper-cut.mp3")
        sound.play()
      }
    
      componentDidMount() {
        fetch("https://chuck-norris-quote-generator.herokuapp.com/jokes")
          .then(data => data.json())
          .then(JSONdata => {
            console.log(JSONdata)
            this.setState({ jokes: JSONdata.data.jokes })
          })
      }

    return (
        <div>
            <h1>Chuck Norris</h1>
        </div>
    )
}
