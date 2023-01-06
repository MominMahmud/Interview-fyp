import React from 'react'

export default function Card(props) {
  return (
    <div className="card">
    <div className="card-body">
      <h5 className="card-title">{props.cardTitle}</h5>
      <p className="card-text">
        {props.cardText}
      </p>
      <div class="progress">
        <div
          class="progress-bar progress-bar-striped progress-bar-animated"
          role="progressbar"
          aria-valuenow="60"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      <a href="/candidates" class="btn btn-primary">
        View Candidates
      </a>
    </div>
  </div>

  )
}
