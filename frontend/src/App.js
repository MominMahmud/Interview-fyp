import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Dashboard from "./pages/dashboard/Dashboard";
import Candidates from "./pages/candidates/Candidates";
import CreateJob from "./pages/JobApplication/CreateJob"
import JobApplication from "./pages/JobApplication/JobApplication"
import Profile from "./components/profile/Profile";
import Navbar from "./components/side-nav/Navbar";
import Answers from "./interview/qna/Answers";
import Header from "./components/header/Header";

function App() {
  return (
    <>

      <Router>
        <Switch>
          <Route exact path="/">
            <Header header="Dashboard" />
            <Profile />
            <Navbar />
            <Dashboard />
          </Route>
          <Route path="/candidates">
            <Profile />
            <Navbar />
            <Header header="Candidates" />
            <Candidates />
          </Route>
          <Route path="/interview/:id">
            <Answers></Answers>
          </Route>
          <Route path="/application">
            <JobApplication></JobApplication>
          </Route>
          <Route path="/create/job">
            <Profile />
            <Navbar />
            <Header header="Create Job" />
            <CreateJob></CreateJob>
          </Route>
        </Switch>
      </Router>
    </>
  );
}

export default App;