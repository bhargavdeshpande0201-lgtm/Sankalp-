# Staff/Teacher Dashboard Access Guide

## Overview
Staff and teacher users have access to a comprehensive management dashboard with full complaint management capabilities. This document explains all the features available to staff members.

---

## Staff Dashboard Access

### Automatic Redirection
When a staff/teacher user clicks the **"Dashboard"** link after logging in, they are automatically redirected to the **Admin Dashboard** (not the student dashboard).

**Login Flow for Staff:**
1. User logs in as "Teacher/Staff"
2. Enters staff credentials (e.g., staff1 / Staff123456)
3. Clicks "Dashboard"
4. System detects `user.is_staff = True`
5. Redirects to Admin Dashboard at `/admin-dashboard`

---

## Staff Features

### 1. Admin Dashboard (`/admin-dashboard`)

**View All Complaints**
- See all complaints in the system
- Status: Pending, In Progress, Resolved, Rejected
- Priority: High, Medium, Low
- Category-based filtering
- Pagination (15 complaints per page)

**Key Controls:**
- **Filter by Status:** Dropdown to see specific status complaints
- **Filter by Category:** Filter complaints by department/issue type
- **Filter by Priority:** See high, medium, or low priority items
- **Quick Edit:** Edit button on each complaint

**Dashboard Statistics:**
- Total Complaints count
- Pending Issues (need attention)
- Active Users registered
- Resolution Rate percentage
- Category Breakdown chart
- High Priority Complaint count

---

### 2. Manage Users (`/admin/users`)

**View All Users**
- See all registered users in the system
- User information: name, email, username, join date, user type
- Filter by user type:
  - **Staff/Teachers:** All users with is_staff=True
  - **Students:** All regular users
  - **Admin:** Superuser accounts

**Statistics:**
- Total Users count
- Staff Count
- Student Count
- Admin Count

**Pagination:** 20 users per page

**What Staff Can See:**
- User email addresses
- Account creation dates
- User roles and permissions
- Account status (active/inactive)

**Note:** Bulk user management operations (enable/disable, role changes) may require superuser privileges.

---

### 3. Reports (`/admin/reports`)

**View Complaint Statistics**
- Total complaints in system
- Breakdown by Status (Pending, In Progress, Resolved, Rejected)
- Resolution rate (resolved / total)
- Resolution rate percentage

**Category Analysis**
- Count of complaints per category
- Percentage distribution
- Visual representation

**Priority Analysis**
- Count of complaints per priority level
- Low, Medium, High breakdown
- Percentage for each level

**Top Reporters**
- Top 5 users who submitted most complaints
- Their complaint counts
- Helps identify high-engagement users

**Data Export:**
- Reports can be used for auditing
- Useful for identifying trends
- Monthly/yearly analysis possible

---

### 4. Activity Log (`/admin/activity`)

**Recent Complaints**
- Latest 10 complaints submitted
- Shows submission timestamps
- Status indicators
- Quick access to full details

**Recent Comments/Updates**
- Latest 15 comments from staff and users
- Shows who commented and when
- Comment content preview
- Easy tracking of system activity

**Use Cases:**
- Monitor system activity
- See what other staff members are doing
- Follow up on recent updates
- Track user feedback

---

### 5. Edit Complaint (`/admin-dashboard` → Click Edit)

**Edit Complaint Details:**

**Status Management**
- Change status: Pending → In Progress → Resolved/Rejected
- Automatic logging of status changes
- Status history visible in comments

**Priority Changes**
- Adjust priority: Low → Medium → High
- Update priority based on severity
- Affects complaint sorting and visibility

**Add Staff Comments**
- Add internal notes about complaint
- Comments marked as from staff (is_staff=True)
- Visible to both staff and users
- Professional communication channel

**Comment History**
- See all comments (user and staff)
- Timestamps for each comment
- Identify who last updated the complaint
- Full audit trail

**Example Staff Workflow:**
1. Review complaint details
2. Check complaint status and history
3. Change status to "In Progress" when starting work
4. Add comment describing actions taken
5. Update priority if needed
6. Mark as "Resolved" when issue is fixed
7. Add final comment with resolution details

---

## Access Control Summary

### Staff Can Access:
✅ Admin Dashboard (`/admin-dashboard`)
✅ Manage Users (`/admin/users`)
✅ Reports (`/admin/reports`) 
✅ Activity Log (`/admin/activity`)
✅ Edit Complaints (via Edit buttons)
✅ View all system complaints
✅ Add comments to complaints
✅ Change complaint status and priority
✅ Filter and search complaints

### Staff CANNOT Do:
❌ Create/delete users (requires superuser)
❌ Assign admin roles (requires superuser)
❌ System-wide settings (requires superuser)
❌ Access other staff member's private data
❌ Delete complaints (only staff can edit/comment)

---

## Navigation

### From Login Page:
1. Select "Teacher/Staff" role
2. Enter staff username and password
3. Click "Sign In"
4. Click "Dashboard" or "Admin Dashboard"

### From Staff Dashboard:
- **View Complaints:** Main dashboard shows all complaints
- **Manage Users:** "Manage Users" button (top right)
- **View Reports:** "Reports" button (top right)
- **Check Activity:** "Activity" button (top right)
- **Edit Complaint:** Click "Edit" button on any complaint row
- **Back to Dashboard:** Click "Admin Dashboard" link

---

## Workflow Example: Resolving a Complaint

### Step 1: Identify Problem Complaint
1. Go to Admin Dashboard
2. See complaint with status "Pending"
3. Click "Edit" button on complaint

### Step 2: Review Details
1. View complaint text and category
2. Check existing comments
3. Note priority level
4. Review user information

### Step 3: Assign Priority
1. Change priority if needed (e.g., increase to "High")
2. Save changes

### Step 4: Update Status & Comment
1. Change status to "In Progress"
2. Add comment: "Started investigating, will contact user by email"
3. Click "Update Complaint"

### Step 5: Work on Issue
1. (Offline work/resolution)

### Step 6: Mark Resolved
1. Go back to Edit Complaint
2. Change status to "Resolved"
3. Add comment: "Issue resolved by installing new software license. User notified."
4. Save changes

### Step 7: Monitor Reports
1. Go to Reports
2. Check resolution rate
3. Verify complaint appears as "Resolved"

---

## Best Practices for Staff

✓ **Communication:**
- Always add comments explaining actions
- Keep users informed of status changes
- Professional and courteous language

✓ **Status Management:**
- Change to "In Progress" as soon as you start work
- Update status promptly when resolved
- Use "Rejected" only for invalid complaints

✓ **Priority Handling:**
- Re-prioritize based on severity and impact
- Keep high-priority issues visible
- Regular reviews of all pending complaints

✓ **Documentation:**
- Leave detailed comments for audit trail
- Explain decisions and resolutions
- Help other staff understand context

✓ **User Management:**
- Review user list regularly
- Monitor active vs. inactive accounts
- Help identify problematic accounts (admin)

---

## Troubleshooting

### "Access Denied" Error
- **Cause:** User account is missing `is_staff = True`
- **Solution:** Contact admin to set staff privilege

### Can't See Edit Button
- **Cause:** Account may not have staff privileges
- **Solution:** Verify in Admin panel that is_staff is checked

### Dashboard Shows "Pending" but Should be Resolved
- **Cause:** Status wasn't saved properly
- **Solution:** Click Edit again and verify status is actually updated

### Comments Not Appearing
- **Cause:** Comment may not have been saved
- **Solution:** Make sure to click "Update Complaint" button

### Can't Change User Roles
- **Cause:** Staff accounts can view but not edit user roles
- **Solution:** Contact superuser/admin to change user roles

---

## Demo Credentials

**Staff Login:**
```
Username: staff1
Password: Staff123456
```

**What You Can Do After Login:**
1. Access Admin Dashboard
2. View all complaints
3. Filter by status, category, priority
4. Edit any complaint
5. Add comments
6. View Reports with statistics
7. Check Activity log
8. Manage Users view
9. Test all features without restrictions

---

## Key Statistics Tracked

### Dashboard Cards
- **Total Complaints** - All complaints ever submitted
- **Pending Issues** - Complaints needing attention
- **Active Users** - Total registered users
- **Resolution Rate** - % of resolved / total complaints

### Report Analytics
- **Complaint Status Distribution** - Visual breakdown
- **Category Statistics** - Most common issue types
- **Priority Statistics** - High/Medium/Low breakdown
- **Top Reporters** - Most active complaint submitters

### Activity Tracking
- **Recent Complaints** - Latest 10 submissions
- **Recent Comments** - Latest 15 updates
- **User Actions** - Who did what and when

---

## URL Reference

| Feature | URL |
|---------|-----|
| Dashboard | `/admin-dashboard` |
| Manage Users | `/admin/users` |
| Reports | `/admin/reports` |
| Activity | `/admin/activity` |
| Edit Complaint | `/complaint/<id>/admin-edit` |

---

## API & Integration Notes

**For Developers:**
- All endpoints check `request.user.is_staff`
- Redirect to `/dashboard` if not staff
- Error message shown to unauthorized users
- Comments marked with `is_staff=True` automatically
- Status changes logged in comments

---

## Support & Documentation

For additional help:
- Check TROUBLESHOOTING.md
- Review QUICK_REFERENCE.md
- Contact system admin
- Check inline code comments in views.py

---

## Version Information
- Django: 4.2+
- Bootstrap: 5.0+
- Database: SQLite (local) / PostgreSQL (production)
- Date Created: 2024

