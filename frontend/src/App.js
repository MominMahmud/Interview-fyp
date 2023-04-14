import React, { useState, useEffect } from "react";
import Components from "./components/Components";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Dashboard from "./pages/dashboard/Dashboard";
import Candidates from "./pages/candidates/Candidates";
import CreateJob from "./pages/JobApplication/CreateJob"
import JobApplication from "./pages/JobApplication/JobApplication"

import Answers from "./interview/qna/Answers";

function App() {
  return (
    <>
      <Router>
        <Switch>
          <Route exact path="/">
            <Components header="Dashboard" />
            <Dashboard />
          </Route>
          <Route path="/candidates">
            <Components header="Candidates" />
            <Candidates />
          </Route>
          <Route path="/interview/:id">
            <Answers></Answers>
          </Route>
          <Route path="/application">
            <JobApplication></JobApplication>
          </Route>
          <Route path="/create/job">
            <Components header="Create Job" />
            <CreateJob></CreateJob>
          </Route>
        </Switch>
      </Router>
    </>
  );
}

export default App;