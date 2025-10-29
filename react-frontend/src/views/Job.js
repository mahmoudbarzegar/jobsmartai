/*!

=========================================================
* Argon Dashboard React - v1.2.4
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2024 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// reactstrap components
import React, { useEffect, useState } from "react";

import {
  Card,
  CardHeader,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  DropdownToggle,
  Media,
  Table,
  Container,
  Row,
  Button,
  Modal,
  ModalBody,
  ModalFooter,
} from "reactstrap";
// core components
import Header from "components/Headers/Header.js";

const Job = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [openDropdown, setOpenDropdown] = useState(null);
  const [selectedJob, setSelectedJob] = useState({
    title: "",
    description: "",
  });
  const [modalOpen, setModalOpen] = React.useState(false);

  // const handleViewCoverLetter = (jobId) => {
  //   setIsModalOpen(openDropdown === jobId ? null : jobId);
  // };

  const closeModal = () => {
    setSelectedJob(null);
  };

  const handleViewJobDetail = (title, description) => {
    setModalOpen(!modalOpen);
    setSelectedJob({
      title: title,
      description: description,
    });
  };

  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:8000/api/jobs")
      .then((res) => res.json())
      .then((data) => {
        setJobs(data.result.data);
        setLoading(false);
      })
      .catch((err) => console.error("Error fetching resumes:", err));
  }, []);
  return (
    <>
      <Header />
      {/* Page content */}
      <Container className="mt--7" fluid>
        <Row className="mt-5">
          <div className="col">
            <Card className="shadow">
              <CardHeader className="bg-transparent border-0">
                <div className="col-12">
                  <Button color="info" type="button">
                    Add Job
                  </Button>
                </div>
              </CardHeader>
              <Table className="align-items-center table-flush" responsive>
                <thead className="thead-light">
                  <tr>
                    <th scope="col">Job Name</th>
                    <th scope="col">Score</th>
                    <th scope="col">Resume</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td>
                        <span>Please Wait..........</span>
                      </td>
                    </tr>
                  ) : (
                    jobs.map((job) => (
                      <tr key={job.id}>
                        <th scope="row">
                          <span className="mb-0 text-sm">{job?.title}</span>
                        </th>
                        <th scope="col">{job?.score}</th>
                        <td>
                          <a href={job?.resume_url} target="_blank">
                            View
                          </a>
                        </td>
                        <td className="text-right">
                          <UncontrolledDropdown>
                            <DropdownToggle
                              className="btn-icon-only text-light"
                              href="#pablo"
                              role="button"
                              size="sm"
                              color=""
                              onClick={(e) => e.preventDefault()}
                            >
                              <i className="fas fa-ellipsis-v" />
                            </DropdownToggle>
                            <DropdownMenu className="dropdown-menu-arrow" right>
                              <DropdownItem
                                href="#pablo"
                                onClick={() =>
                                  handleViewJobDetail(
                                    job.title,
                                    job.cover_letter
                                  )
                                }
                              >
                                View Cover Letter
                              </DropdownItem>
                              <DropdownItem
                                href="#pablo"
                                onClick={() =>
                                  handleViewJobDetail(
                                    job.title,
                                    job.description
                                  )
                                }
                              >
                                View Job Detail
                              </DropdownItem>
                            </DropdownMenu>
                          </UncontrolledDropdown>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </Table>
            </Card>
          </div>
        </Row>

        <Modal toggle={() => setModalOpen(!modalOpen)} isOpen={modalOpen}>
          <div className=" modal-header">
            <h5 className=" modal-title" id="exampleModalLabel">
              {selectedJob?.title}
            </h5>
            <button
              aria-label="Close"
              className=" close"
              type="button"
              onClick={() => setModalOpen(!modalOpen)}
            >
              <span aria-hidden={true}>×</span>
            </button>
          </div>
          <ModalBody>
            <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
              {selectedJob?.description}
            </pre>
          </ModalBody>
          <ModalFooter>
            <Button
              color="secondary"
              type="button"
              onClick={() => setModalOpen(!modalOpen)}
            >
              Close
            </Button>
          </ModalFooter>
        </Modal>
      </Container>
    </>
  );
};

export default Job;
