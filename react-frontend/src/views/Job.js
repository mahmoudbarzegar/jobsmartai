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
} from "reactstrap";
// core components
import Header from "components/Headers/Header.js";

const Job = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [openDropdown, setOpenDropdown] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);

  const toggleDropdown = (jobId) => {
    setOpenDropdown(openDropdown === jobId ? null : jobId);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedJob(null);
  };

  const handleViewCoverLetter = (job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
    setOpenDropdown(null);
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
                              onClick={(e) => {
                                e.preventDefault();
                                toggleDropdown(job.id);
                              }}
                            >
                              <i className="fas fa-ellipsis-v" />
                            </DropdownToggle>
                            {openDropdown === job.id && (
                              <DropdownMenu
                                className="dropdown-menu-arrow"
                                right
                              >
                                <DropdownItem
                                  href="#pablo"
                                  onClick={(e) => {
                                    e.preventDefault();
                                    handleViewCoverLetter(job);
                                  }}
                                >
                                  {" "}
                                  View Cover Letter
                                </DropdownItem>

                                <DropdownItem
                                  href="#pablo"
                                  onClick={(e) => e.preventDefault()}
                                >
                                  View Job Detail
                                </DropdownItem>
                              </DropdownMenu>
                            )}
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

        {/* Modal */}
        {isModalOpen && selectedJob && (
          <div className="fixed inset-0 z-50 overflow-y-auto">
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
              onClick={closeModal}
            ></div>

            {/* Modal Content */}
            <div className="flex items-center justify-center min-h-screen p-4">
              <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
                {/* Modal Header */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                      {selectedJob.title}
                    </h2>
                    <p className="text-gray-600 mt-1">{selectedJob.company}</p>
                  </div>
                  <button
                    onClick={closeModal}
                    className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
                  >
                    ×
                  </button>
                </div>

                {/* Modal Body */}
                <div className="border-t border-gray-200 pt-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Cover Letter
                  </h3>
                  <div className="bg-gray-50 rounded-lg p-4 whitespace-pre-wrap text-gray-700">
                    {selectedJob.cover_letter}
                  </div>
                </div>

                {/* Modal Footer */}
                <div className="mt-6 flex justify-end gap-3">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition-colors"
                  >
                    Close
                  </button>
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    Edit Cover Letter
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Click outside dropdown to close */}
        {openDropdown && (
          <div
            className="fixed inset-0 z-0"
            onClick={() => setOpenDropdown(null)}
          ></div>
        )}
      </Container>
    </>
  );
};

export default Job;
