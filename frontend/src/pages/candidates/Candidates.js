import React, { useState, useEffect } from "react";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";

export default function Candidates() {
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "1px solid #000",
    boxShadow: 2,
    pt: 2,
    px: 4,
    pb: 3,
  };
  const queryParameters = new URLSearchParams(window.location.search);
  const id = queryParameters.get("id");
  const [job, setJob] = useState("");
  var [candidates, setCandidates] = useState([]);
  var url = "http://localhost:90/jobs";
  var url2 = "http://localhost:90/candidates";
  url = url + "/" + id;
  console.log(url);
  useEffect(() => {
    axios
      .get(url)
      .then((res) => {
        console.log(res.data);
        setJob(res.data);
        url2 = url2 + "/" + res.data;
      })
      .then(() => {
        axios.get(url2).then(async (cand) => {
          await setCandidates(cand.data);
        });
      });
  }, []);

  console.log(candidates);

  //console.log(candidates[0].name)
  const [candidateID,setID]=useState({});
  const [candidateResp,setCandidateResp] = useState({
    name: "",
    email: "",
    age: "",
    experience: "",
    status: "0",
    ranking: "0",
    score: "0",
    appliedfor: "",
    res:[]
  });
  const [open, setOpen] = React.useState(false);
  


  const handleClose = (params) => {
    console.log(params);
    setOpen(false);
  };
  const columns = [
    {
      field: "_id",
      headerName: "id",
      width: 50,
      editable: true,
    },

    {
      field: "name",
      headerName: "Name",
      width: 150,
      editable: true,
    },
    {
      field: "age",
      headerName: "Age",
      type: "string",
      width: 150,
      editable: true,
    },
    {
      field: "experience",
      headerName: "Experience",
      type: "string",
      width: 110,
      editable: true,
    },
    {
      field: "status",
      headerName: "Status",
      type: "string",
      sortable: true,
      width: 100,
    },

    {
      field: "ranking",
      headerName: "Rank",
      type: "string",
      sortable: true,
      width: 100,
    },

    {
      field: "action",
      headerName: "Action",
      width: 150,
      sortable: false,
      renderCell: (params) => {
        const onClick = (e) => {
          setOpen(true);

          e.stopPropagation(); // don't select this row after clicking

          const api = params.api;
          const thisRow = {
            name: "",
            email: "",
            age: "",
            experience: "",
            status: "0",
            ranking: "0",
            score: "0",
            appliedfor: "",
            res:[]

          };

          api
            .getAllColumns()
            .filter((c) => c.field !== "__check__" && !!c)
            .forEach(
              (c) => (thisRow[c.field] = params.getValue(params.id, c.field))
            );
            setID(thisRow)
            setCandidateResp(candidates.filter(async (data)=>{
              return await data._id==thisRow._id;
            }))
            

          return alert(JSON.stringify(thisRow, null, 4));
        };

        return (
          <div>
            <button className="btn btn-primary" onClick={onClick}>
              Responses
            </button>
            <Modal
              open={open}
              onClose={handleClose}
              aria-labelledby="child-modal-title"
              aria-describedby="child-modal-description"
            >
              <Box sx={{ width: 200, ...style }}>
                <h2 id="child-modal-title">Responses</h2>
                 {console.log(candidateResp[0])}
               {candidateResp[0]["res"].map((n) => 
               <p key={n}>{n}</p>  )} 
                <p id="child-modal-description">{candidateID["res"]}</p>
                <button className="btn btn-primary" onClick={handleClose}>
                  Close
                </button>
              </Box>
            </Modal>
          </div>
        );
      },
    },
  ];
  return (
    <div style={{ height: 500 }} className="table">
      <DataGrid
        rows={candidates}
        columns={columns}
        pageSize={30}
        checkboxSelection
        disableSelectionOnClick
        getRowId={(row) => row._id}
      />
    </div>
  );
}
