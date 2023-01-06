import React, { useState, useEffect } from "react";
import Components from "./components/Components";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Dashboard from './pages/dashboard/Dashboard'
import Candidates from "./pages/candidates/Candidates";
import Interview from "./interview/Interview";

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
          <Router path='/interview'>
            <Interview></Interview>
          </Router>
        </Switch>
      </Router>
    </>
  );
}

export default App;
