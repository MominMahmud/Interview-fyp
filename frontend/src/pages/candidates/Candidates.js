import React, { useState, useEffect } from "react";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Chart from "chart.js/auto";
import { BarChart } from "../../components/charts/Barchart";
const Data = [
  {
    id: 1,
    year: 2016,
    userGain: 80000,
    userLost: 823,
  },
  {
    id: 2,
    year: 2017,
    userGain: 45677,
    userLost: 345,
  },
  {
    id: 3,
    year: 2018,
    userGain: 78888,
    userLost: 555,
  },
  {
    id: 4,
    year: 2019,
    userGain: 90000,
    userLost: 4555,
  },
  {
    id: 5,
    year: 2020,
    userGain: 4300,
    userLost: 234,
  },
];
export default function Candidates() {
  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width:768,
    bgcolor: "background.paper",
    border: "1px solid #000",
    boxShadow: 2,
    pt: 2,
    px: 4,
    pb: 3,
    overflow:'scroll',
    maxHeight: 500,
    display:'block'
  };
  const [chartData, setChartData] = useState({});
  const [chartData2, setChartData2] = useState({});
  const queryParameters = new URLSearchParams(window.location.search);
  const id = queryParameters.get("id");
  const [job, setJob] = useState("");
  var [candidates, setCandidates] = useState([]);
  var url = "http://localhost:90/jobs";
  var url2 = "http://localhost:90/candidates";
  url = url + "/" + id;
  console.log(url);

  const [emotions,setEmotions]=useState({})
  useEffect(() => {
    axios
      .get(url)
      .then((res) => {
        console.log(res.data);
        setJob(res.data);
        url2 = url2 + "/" + res.data;
      })
      .then(() => {
        axios.get(url2).then((cand) => {
          setCandidates(cand.data);
        });
      })
  }, []);

  var emotionss
  console.log(candidates);

  //console.log(candidates[0].name)
  const [candidateID, setID] = useState({});
  const [candidateResp, setCandidateResp] = useState([{}]);
  const [open, setOpen] = React.useState(false);


  const handleClose = (params) => {
    console.log(params);
    setOpen(false);
    setCandidateResp([
      {
        name: "",
        email: "",
        age: "",
        experience: "",
        status: "0",
        ranking: "0",
        score: "0",
        appliedfor: "",
        res: [],
      },
    ]);
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
          e.stopPropagation(); // don't select this row after clicking

          const api = params.api;
          const thisRow = {};

          api
            .getAllColumns()
            .filter((c) => c.field !== "__check__" && !!c)
            .forEach(
              (c) => (thisRow[c.field] = params.getValue(params.id, c.field))
            );
            axios.get('http://localhost:90/gav/'+thisRow._id,).then( (res)=>{

            console.log(res.data)
              setEmotions(res.data)
               emotionss = res.data
              console.log(emotions)

              setChartData({
                labels: emotions[0]?.labelsA,
                datasets: [
                  {
                    label: "Audio Emotions",
                    data: emotions[0]?.valuesA,
                    backgroundColor: [
                      "rgba(75,192,192,1)",
                      "&quot;#ecf0f1",
                      "#50AF95",
                      "#f3ba2f",
                      "#2a71d0",
                      "red",
                      "yellow"
                    ],
                    borderColor: "black",
                    borderWidth: 2,
                  },
                ],

                text:"Audio Emotions"
              })
              setChartData2({
                labels: emotions[0]?.labelsV,
                datasets: [
                  {
                    label: "Audio Emotions",
                    data: emotions[0]?.valueV,
                    backgroundColor: [
                      "rgba(75,192,192,1)",
                      "&quot;#ecf0f1",
                      "#50AF95",
                      "#f3ba2f",
                      "#2a71d0",
                      "red",
                      "yellow"
                    ],
                    borderColor: "black",
                    borderWidth: 2,
                  },
                ],

                text:"Video Emotions"
              })
              

            }).then(()=>{

              setOpen(true);
            })
          return ;
        };

        return (
          <div>
            {
              console.log('Data For Chart 2: ', chartData2)
            }
            <button className="btn btn-primary" onClick={onClick}
              >
              Responses
            </button>
            <Modal
              open={open}
              onClose={handleClose}
              aria-labelledby="child-modal-title"
              aria-describedby="child-modal-description"
            >
              <Box sx={{ width: 800, ...style }}>
                <BarChart chartData={chartData}></BarChart>
                <BarChart chartData={chartData2}></BarChart>
                <h5>Silence Gaps:</h5> {emotions[0]?.silence.map((item)=>{

                  return (<p>{item}</p>)
                })}
                <h5>Speech to Silence Ratio: </h5><p>{emotions[0]?.StoSR}</p>
                <h5>Average silence Duration: </h5><p>{emotions[0]?.avgSDUR}</p>
                <h5>Average silence duration per minute: </h5><p>{emotions[0]?.avgSPM}</p>
                <h5>Number of unique words:</h5> <p>{emotions[0]?.numUnique}?</p>
                <h5>Unique words to total number of words:</h5> <p>{emotions[0]?.uniqueWords}</p>
                <h5>Rate of words per minute: </h5><p>{emotions[0]?.rateWPM}</p>
                <h5>Sentiment:</h5> <p>{emotions[0]?.sentiment}</p>
                
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
