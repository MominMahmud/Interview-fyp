import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import {useState,useEffect} from "react"
import axios from "axios";
import { BarChart } from "../../components/charts/Barchart";
export default function Candidates() {
  const Data = [
    {
      id: 1,
      year: 2016,
      userGain: 80000,
      userLost: 823
    },
    {
      id: 2,
      year: 2017,
      userGain: 45677,
      userLost: 345
    },
    {
      id: 3,
      year: 2018,
      userGain: 78888,
      userLost: 555
    },
    {
      id: 4,
      year: 2019,
      userGain: 90000,
      userLost: 4555
    },
    {
      id: 5,
      year: 2020,
      userGain: 4300,
      userLost: 234
    }
  ];
  const [chartData, setChartData] = useState({
    labels: Data.map((data) => data.year), 
    datasets: [
      {
        label: "Users Gained ",
        data: Data.map((data) => data.userGain),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "&quot;#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 2
      }
    ]})
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
  const [candidateResp,setCandidateResp] = useState([{

  }]);
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "firstName",
      headerName: "First name",
      width: 150,
      editable: true,
    },
    {
      field: "lastName",
      headerName: "Last name",
      width: 150,
      editable: true,
    },
    {
      field: "age",
      headerName: "Age",
      type: "number",
      width: 110,
      editable: true,
    },
    {
      field: "fullName",
      headerName: "Full name",
      description: "This column has a value getter and is not sortable.",
      sortable: false,
      width: 160,
      valueGetter: (params) =>
        `${params.getValue(params.id, "firstName") || ""} ${
          params.getValue(params.id, "lastName") || ""
        }`,
    },
    {
      field: "action",
      headerName: "Action",
      width: 120,
      sortable: false,
      renderCell: (params) => {
        const onClick = (e) => {
          e.stopPropagation(); // don't select this row after clicking

          const api = params.api;
          const thisRow = {};

          api
            .getAllColumns()
            .filter((c) => c.field !== "__check__" && !!c)
            .forEach(
              (c) => (thisRow[c.field] = params.getValue(params.id, c.field))
            );

          return alert(JSON.stringify(thisRow, null, 4));
        };

        return (
          <div>
            <button className="btn btn-primary" onClick={handleOpen}>
              Responses
            </button>
            <Modal
              hideBackdrop
              open={open}
              onClose={handleClose}
              aria-labelledby="child-modal-title"
              aria-describedby="child-modal-description"
            >
              <Box sx={{ width: 200, ...style }}>
                <h2 id="child-modal-title">Responses</h2>

                <BarChart chartData={chartData}></BarChart>
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
        pageSize={5}
        checkboxSelection
        disableSelectionOnClick
      />
    </div>
  );
}
