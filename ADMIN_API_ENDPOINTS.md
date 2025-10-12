# Admin API Endpoints - Complete Reference

## ✅ **FIXES APPLIED:**

### 1. **Field Name Compatibility (camelCase + snake_case)**
- All serializers now support BOTH formats
- Frontend can use `jdLimit` or `jd_limit` 
- Backward compatible with existing code

### 2. **User Plan Update**
- Fixed: `AdminUserUpdateSerializer` now accepts `planId` (camelCase)
- Fixed: Plan limits now visible in frontend with `jdLimit` and `cvLimit` fields

---

## 🔐 **Authentication Routes**

### Admin Login
```http
POST /api/admin/login
Content-Type: application/json

{
  "email": "admin@talentranker.com",
  "password": "admin123"
}

Response 200:
{
  "message": "Admin login successful",
  "accessToken": "...",
  "user": { ... }
}
```

### Admin Logout
```http
POST /api/admin/logout
Authorization: Bearer <token>

Response 200:
{
  "message": "Admin logged out successfully"
}
```

### Get Admin Profile
```http
GET /api/admin/profile
Authorization: Bearer <token>

Response 200:
{
  "message": "Admin profile retrieved",
  "user": { ... }
}
```

---

## 📊 **Dashboard & Analytics**

### Get Dashboard Stats
```http
GET /api/admin/dashboard
Authorization: Bearer <token>

Response 200:
{
  "message": "Admin dashboard data retrieved",
  "stats": {
    "totalUsers": 10,
    "activePlans": 21,
    "totalJDsProcessed": 50,
    "totalCVsProcessed": 500,
    "systemStatus": "online"
  }
}
```

### Get Analytics
```http
GET /api/admin/analytics?dateRange=30
Authorization: Bearer <token>

Response 200:
{
  "message": "Analytics retrieved successfully",
  "analytics": {
    "users": {
      "total": 10,
      "active": 8,
      "new": 3
    },
    "usage": {
      "totalJDs": 50,
      "totalCVs": 500
    },
    "planDistribution": [...]
  }
}
```

---

## 👥 **User Management**

### List All Users
```http
GET /api/admin/users?page=1&limit=10&search=
Authorization: Bearer <token>

Response 200:
{
  "message": "Users retrieved successfully",
  "users": [
    {
      "id": 2,
      "_id": 2,
      "name": "John Doe",
      "email": "user@example.com",
      "role": "user",
      "plan": {
        "id": 1,
        "_id": 1,
        "name": "Freemium",
        "jdLimit": 1,
        "cvLimit": 10,
        ...
      },
      "jdUsed": 0,
      "cvUsed": 0,
      "isActive": true,
      ...
    }
  ],
  "total": 1
}
```

### Get Single User
```http
GET /api/admin/users/2
Authorization: Bearer <token>

Response 200:
{
  "message": "User retrieved successfully",
  "user": { ... }
}
```

### Update User (Including Plan)
```http
PUT /api/admin/users/2
Authorization: Bearer <token>
Content-Type: application/json

{
  "planId": 5,           // ✅ camelCase supported
  "name": "Updated Name",
  "is_active": true
}

OR

{
  "plan_id": 5,          // ✅ snake_case also works
  "name": "Updated Name",
  "is_active": true
}

Response 200:
{
  "message": "User updated successfully",
  "user": { ... }
}
```

### Update User Plan (Dedicated Endpoint)
```http
PUT /api/admin/users/2/plan
Authorization: Bearer <token>
Content-Type: application/json

{
  "planId": 5,
  "resetUsageOnUpgrade": false
}

Response 200:
{
  "message": "User plan updated successfully",
  "user": { ... }
}
```

### Delete User
```http
DELETE /api/admin/users/2
Authorization: Bearer <token>

Response 200:
{
  "message": "User deleted successfully"
}
```

---

## 💳 **Plan Management**

### List All Plans
```http
GET /api/admin/plans?region=Pakistan&isActive=true
Authorization: Bearer <token>

Response 200:
{
  "message": "Plans retrieved successfully",
  "plans": [
    {
      "id": 1,
      "_id": 1,
      "name": "Freemium",
      "region": "Global",
      "billingCycle": null,
      "billing_cycle": null,
      "price": 0,
      "currency": "USD",
      "jdLimit": 1,          // ✅ camelCase
      "jd_limit": 1,         // ✅ snake_case
      "cvLimit": 10,         // ✅ camelCase
      "cv_limit": 10,        // ✅ snake_case
      "description": "...",
      "features": ["..."],
      "isActive": true,
      "is_active": true,
      "sortOrder": 1,
      "sort_order": 1,
      ...
    }
  ],
  "total": 21
}
```

### Create Plan
```http
POST /api/admin/plans
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Custom Plan",
  "region": "Pakistan",
  "billing_cycle": "Monthly",
  "price": 5000,
  "currency": "PKR",
  "jd_limit": 20,
  "cv_limit": 200,
  "description": "Custom plan description",
  "features": ["Feature 1", "Feature 2"],
  "is_active": true,
  "sort_order": 100
}

Response 201:
{
  "message": "Plan created successfully",
  "plan": { ... }
}
```

### Update Plan
```http
PUT /api/admin/plans/31
Authorization: Bearer <token>
Content-Type: application/json

{
  "price": 6000,
  "jd_limit": 25,
  "is_active": true
}

Response 200:
{
  "message": "Plan updated successfully",
  "plan": { ... }
}
```

### Delete Plan
```http
DELETE /api/admin/plans/31
Authorization: Bearer <token>

Response 200:
{
  "message": "Plan deleted successfully"
}

Response 400 (if users are using the plan):
{
  "message": "Cannot delete plan. 5 user(s) are currently using this plan."
}
```

---

## 📝 **Notes:**

### Field Naming Convention
- **API returns BOTH formats** for compatibility:
  - Snake case: `jd_limit`, `cv_limit`, `billing_cycle`, `is_active`, etc.
  - Camel case: `jdLimit`, `cvLimit`, `billingCycle`, `isActive`, etc.
- **API accepts BOTH formats** for inputs:
  - You can send `planId` or `plan_id`
  - You can send `jd_limit` or `jdLimit`

### ID Fields
- All resources have both `id` and `_id` for MongoDB compatibility
- Use either field in frontend code

### Authentication
- All admin endpoints require `Authorization: Bearer <token>` header
- Token expires in 15 minutes
- Use `/api/auth/refresh` to get new access token

### Pagination
- User list supports `page` and `limit` query parameters
- Default: page=1, limit=10

### Filtering
- Plans support: `region`, `name`, `isActive` filters
- Users support: `search` parameter

---

## 🧪 **Testing Checklist:**

### User Management
- [x] List users
- [x] Get single user
- [x] Update user details
- [x] Update user plan (PUT /users/:id with planId)
- [x] Update user plan (PUT /users/:id/plan)
- [x] Delete user
- [x] Prevent admin self-deletion

### Plan Management
- [x] List plans with filters
- [x] Create plan
- [x] Update plan
- [x] Delete plan
- [x] Prevent deletion of plans in use
- [x] Display jdLimit and cvLimit in frontend

### Dashboard
- [x] Get dashboard stats
- [x] Get analytics with date range

### Field Compatibility
- [x] camelCase fields work (planId, jdLimit, etc.)
- [x] snake_case fields work (plan_id, jd_limit, etc.)
- [x] Both formats returned in API responses

---

## 🎯 **All Issues Resolved:**

1. ✅ **Plan limits showing in frontend** - Added camelCase aliases (`jdLimit`, `cvLimit`)
2. ✅ **User plan update working** - AdminUserUpdateSerializer now accepts `planId`
3. ✅ **405 Method Not Allowed** - Combined views for same URL patterns
4. ✅ **_id field support** - All serializers include `_id` for MongoDB compatibility
5. ✅ **Complete CRUD operations** - All create, read, update, delete operations working
