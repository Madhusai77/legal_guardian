# RBI/SBI Debt Collection & Fair Practices Code (FPC) - Structured Context

RBI_FAIR_PRACTICES_CODE = """
### 1. CONDUCT DURING DEBT COLLECTION (RBI/FPC/2024)
Lenders and recovery agents are strictly prohibited from:
- Using minatory, abusive, or obscene language.
- Threatening physical force or intimidation against the borrower or their family.
- Publicly shaming the borrower or violating their privacy (e.g., social media shaming).
- Making misleading representations about the debt or legal consequences.

### 2. PERMISSIBLE CONTACT HOURS
- Lenders and agents may only contact borrowers between **8:00 AM and 7:00 PM**.
- Contact outside these hours constitutes a violation of the RBI Fair Practices Code.

### 3. THIRD-PARTY CONTACT RESTRICTIONS
- Agents MUST interact ONLY with the borrower or the guarantor.
- APPROACHING relatives, friends, referees, or colleagues is STRICTLY PROHIBITED.
- Disclosing the borrower's debt to third parties is a violation of financial privacy.

### 4. IDENTIFICATION AND DOCUMENTATION
- Recovery agents must carry an official Identity Card issued by the lender.
- Agents must carry a copy of the formal recovery notice and an authorization letter.
- Borrowers have the right to demand these documents before any interaction.

### 5. SENSITIVE OCCASIONS
- Debt collection activities must be avoided during times of bereavement, family emergencies, or major family festivals/weddings.

### 6. CALL RECORDING AND TRANSPARENCY
- Banks/Lenders must record all recovery calls and inform the borrower of the recording.
- Detailed logs of contact frequency and timing must be maintained for regulatory audit.

### 7. INTEREST AND CHARGES (Update April 2024)
- Interest must be charged only from the actual date of disbursement.
- Penal charges must be reasonable and explicitly mentioned in the loan agreement.
- Lenders must refund any excess interest collected through unfair practices.

### 8. GRIEVANCE REDRESSAL MECHANISM
- Every lender must have a Board-approved grievance redressal system.
- If a formal complaint is filed regarding recovery behavior, the lender should pause recovery until the complaint is addressed, unless proven frivolous.
"""

def get_rbi_context():
    return RBI_FAIR_PRACTICES_CODE
