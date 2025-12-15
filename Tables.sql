CREATE TABLE `tbl_login` (
    `username` VARCHAR(50) NOT NULL PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `role` ENUM('Admin', 'Voter') NOT NULL,
    `status` ENUM('Active', 'Inactive') DEFAULT 'Active'
);

CREATE TABLE `tbl_users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `voter_id` VARCHAR(20) NOT NULL UNIQUE, -- Unique voter ID
    `name` VARCHAR(100) NOT NULL,
    `status` ENUM('Active', 'Inactive') DEFAULT 'Inactive', -- Default to Inactive
    `approved` ENUM('Yes', 'No') DEFAULT 'No', -- Only 'Yes' users can vote
    FOREIGN KEY (`username`) REFERENCES `tbl_login`(`username`) ON DELETE CASCADE
);

CREATE TABLE `tbl_elections` (
    `election_id` INT AUTO_INCREMENT PRIMARY KEY,
    `election_name` VARCHAR(100) UNIQUE NOT NULL,
    `status` ENUM('Ongoing', 'Completed') DEFAULT 'Ongoing'
);

CREATE TABLE `tbl_candidates` (
    `candidate_id` INT AUTO_INCREMENT PRIMARY KEY,
    `voter_id` VARCHAR(20) NOT NULL UNIQUE, -- Ensure candidates have a valid voter ID
    `full_name` VARCHAR(100) NOT NULL,
    `election_id` INT NOT NULL,
    `position` VARCHAR(50) NOT NULL,
    `party` VARCHAR(100) NOT NULL, 
    `symbol_img` VARCHAR(255) NOT NULL, -- Path to candidate's party symbol image file
    `can_img` VARCHAR(255) NOT NULL, -- Path to candidate's image file
    FOREIGN KEY (`election_id`) REFERENCES `tbl_elections`(`election_id`) ON DELETE CASCADE,
);

CREATE TABLE `tbl_votes` (
    `vote_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `election_id` INT NOT NULL,
    `candidate_id` INT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `tbl_users`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`election_id`) REFERENCES `tbl_elections`(`election_id`) ON DELETE CASCADE,
    FOREIGN KEY (`candidate_id`) REFERENCES `tbl_candidates`(`candidate_id`) ON DELETE CASCADE,
    UNIQUE (`user_id`, `election_id`) -- Prevents multiple votes from the same user in an election
);

CREATE TABLE `tbl_results` (
    `result_id` INT AUTO_INCREMENT PRIMARY KEY,
    `election_id` INT NOT NULL,
    `candidate_id` INT NOT NULL,
    `status` ENUM('Declared', 'Pending') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (`election_id`) REFERENCES `tbl_elections`(`election_id`) ON DELETE CASCADE,
    FOREIGN KEY (`candidate_id`) REFERENCES `tbl_candidates`(`candidate_id`) ON DELETE CASCADE
);


