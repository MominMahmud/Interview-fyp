import React, { useState, useEffect } from "react";
import Components from "./components/Components";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Dashboard from './pages/dashboard/Dashboard'
import Candidates from "./pages/candidates/Candidates";
import Interview from "./interview/Interview";
import JobApplication from "./pages/JobApplication/JobApplication";
import CreateJob from "./pages/JobApplication/CreateJob";

function App() {
  return (
    <>
      <Router>
        <Switch>
          <Route exact path='/'>
          <Components header="Dashboard"/>
            <Dashboard/>
          </Route>
          <Route path='/candidates'>
            <Components header="Candidates"/>
            <Candidates/>
          </Route>
          <Route path='/interview/:id'>
            <Interview></Interview>
          </Route>
          <Route path='/application'>
            <JobApplication></JobApplication>
          </Route>
          <Route path='/create/job'>
          <Components header="Create Job"/>
            <CreateJob></CreateJob>
          </Route>
        </Switch>
      </Router>
    </>
  );
}

export default App;
