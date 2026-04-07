import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { BookOpen, Scale, ShieldCheck, Clock, Ban, PhoneOff } from "lucide-react";

const RegulatoryDialog = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="hidden sm:flex border-primary/20 hover:bg-primary/5">
          <BookOpen className="mr-1 h-3.5 w-3.5 text-primary" />
          Regulatory Guidelines
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[85vh] overflow-hidden flex flex-col p-0 border-primary/10">
        <DialogHeader className="p-6 pb-2 bg-gradient-to-br from-primary/5 to-transparent">
          <DialogTitle className="text-xl font-bold flex items-center gap-2">
            <Scale className="h-5 w-5 text-primary" />
            RBI Fair Practices Code & Legal Context
          </DialogTitle>
          <DialogDescription className="text-xs">
            Official guidelines for lenders and recovery agents in India (Updated 2024).
          </DialogDescription>
        </DialogHeader>
        
        <ScrollArea className="flex-1 px-6 py-4">
          <div className="space-y-6 pb-6">
            {/* Section 1 */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold flex items-center gap-2 text-foreground">
                <ShieldCheck className="h-4 w-4 text-green-600" /> 1. Protection Against Coercion
              </h3>
              <p className="text-xs text-muted-foreground leading-relaxed pl-6">
                Lenders and recovery agents are strictly prohibited from using methods that violate your dignity or privacy. This includes any practice that causes public embarrassment or shaming, physical force, or intimidation of any kind.
              </p>
              <div className="pl-6 space-y-1.5">
                <div className="flex gap-2 items-start text-[11px] text-muted-foreground italic bg-muted/30 p-2 rounded-lg">
                   <Ban className="h-3 w-3 text-red-500 mt-0.5" />
                   "Abusive, minatory or obscene language is a direct violation of Clause 1 of the FPC."
                </div>
              </div>
            </div>

            {/* Section 2 */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold flex items-center gap-2 text-foreground">
                <Clock className="h-4 w-4 text-orange-600" /> 2. Communication Windows
              </h3>
              <p className="text-xs text-muted-foreground leading-relaxed pl-6">
                Recovery agents may only contact you or your guarantor during standardized hours.
              </p>
              <ul className="pl-6 space-y-1 text-[11px] list-disc list-inside text-muted-foreground">
                <li>Permissible Hours: <span className="font-bold text-foreground">8:00 AM to 7:00 PM</span></li>
                <li>Contact outside this range is illegal harassment.</li>
                <li>Sensitive occasions (bereavement, emergencies) must be avoided.</li>
              </ul>
            </div>

            {/* Section 3 */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold flex items-center gap-2 text-foreground">
                <PhoneOff className="h-4 w-4 text-primary" /> 3. Third-Party Contact
              </h3>
              <p className="text-xs text-muted-foreground leading-relaxed pl-6">
                Agents must interact <span className="font-bold">ONLY</span> with the borrower or the guarantor. They are NOT permitted to approach relatives, friends, referees, or colleagues.
              </p>
              <p className="text-xs text-muted-foreground leading-relaxed pl-6">
                Disclosing your debt status to anyone other than you or your guarantor is a breach of financial confidentiality laws.
              </p>
            </div>

            {/* Legal Summary */}
            <div className="bg-primary/5 rounded-xl p-4 border border-primary/10 space-y-2">
              <h4 className="text-xs font-bold text-primary flex items-center gap-1.5">
                <Scale className="h-3.5 w-3.5" /> Constitutional Rights (IPC)
              </h4>
              <p className="text-[10px] text-muted-foreground leading-relaxed">
                Beyond RBI guidelines, India's Penal Code protects you from **Criminal Intimidation (Section 503/506)**. Harassment for money, even if owed, is a punishable offense if it involves threats of harm to person or reputation.
              </p>
            </div>

            <p className="text-[10px] text-center text-muted-foreground italic border-t pt-4">
              Our AI Lawyer engine uses this detailed framework to identify and cite specific violations during your simulation.
            </p>
          </div>
        </ScrollArea>
        <div className="p-4 border-t bg-muted/10 flex justify-end">
           <DialogTrigger asChild>
             <Button variant="secondary" size="sm" className="h-8">Close Guidelines</Button>
           </DialogTrigger>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default RegulatoryDialog;
