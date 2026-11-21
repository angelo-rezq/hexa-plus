from pathlib import Path
import json
root=Path('/home/sandbox/hexa-plus')
# Fields are shared by the server validator, forms and table views. Relational FKs stay explicit in SQL.
def f(key,label,type='text',**kw): return dict(key=key,label=label,type=type,**kw)
def mod(table,label,ar,permission,fields,**kw): return dict(table=table,label=label,ar=ar,permission=permission,fields=fields,**kw)
status=lambda options:f('status','Status','select',options=options,required=True)
name=f('name','Name',required=True)
client=f('client_id','Client','relation',relation='clients')
project=f('project_id','Project','relation',relation='projects')
assigned=f('assigned_to','Assigned to','relation',relation='profiles')
notes=f('notes','Notes','textarea')
modules={
'clients':mod('clients','Clients','العملاء','clients',[name,f('company','Company'),f('email','Email','email'),f('phone','Phone / WhatsApp'),f('industry','Industry'),status(['prospect','active','inactive','archived']),f('account_manager_id','Account manager','relation',relation='profiles'),notes]),
'leads':mod('leads','Leads','الفرص البيعية','leads',[f('name','Full name',required=True),f('company','Company'),f('email','Email','email'),f('phone','Phone / WhatsApp'),f('source','Source'),f('service','Interested service'),f('budget','Budget range'),f('timeline','Timeline'),f('description','Project description','textarea'),f('stage','Stage','select',options=['new','contacted','qualified','proposal_sent','negotiation','won','lost'],required=True),f('expected_value_minor','Expected value (EGP)','money'),assigned,f('follow_up_date','Follow-up date','date'),notes],statusKey='stage'),
'projects':mod('projects','Projects','المشروعات','projects',[name,client,f('description','Description','textarea'),f('category','Category'),f('start_date','Start date','date'),f('deadline','Deadline','date'),f('budget_minor','Budget (EGP)','money'),f('manager_id','Project manager','relation',relation='profiles'),status(['planning','in_progress','review','on_hold','completed','cancelled']),f('priority','Priority','select',options=['low','normal','high','urgent']),f('progress','Progress %','number',min=0,max=100),notes]),
'milestones':mod('project_milestones','Milestones','المراحل','projects',[name,project,f('deadline','Deadline','date'),status(['planned','in_progress','completed']),notes]),
'tasks':mod('tasks','Tasks','المهام','tasks',[f('title','Task title',required=True),f('description','Description','textarea'),project,client,assigned,f('deadline','Deadline','date'),f('priority','Priority','select',options=['low','normal','high','urgent']),status(['to_do','in_progress','in_review','completed'])]),
'comments':mod('task_comments','Task comments','تعليقات المهام','tasks',[f('task_id','Task','relation',relation='tasks',required=True),f('body','Comment','textarea',required=True)]),
'project-members':mod('project_members','Project team','فريق المشروع','projects',[f('project_id','Project','relation',relation='projects',required=True),f('profile_id','Team member','relation',relation='profiles',required=True)]),
'team':mod('profiles','Team','الفريق','team',[name,f('email','Email','email',required=True),f('phone','Phone'),f('job_title','Job title'),f('department_id','Department','relation',relation='departments'),f('joining_date','Joining date','date'),status(['active','inactive']),f('role_id','Role','relation',relation='roles',required=True)],noCreate=True),
'departments':mod('departments','Departments','الأقسام','team',[name]),
'services':mod('services','Services','الخدمات','services',[name,f('name_ar','Arabic name'),f('slug','URL slug',required=True),f('division','Division','select',options=['digital','marketing'],required=True),f('description','Description','textarea',required=True),f('benefits','Benefits (one per line)','textarea'),f('deliverables','Deliverables (one per line)','textarea'),f('workflow','Workflow (one per line)','textarea'),f('pricing','Pricing text'),f('show_pricing','Show pricing','boolean'),f('image_url','Image URL','url'),f('featured','Featured','boolean'),f('published','Published','boolean'),f('sort_order','Display order','number')]),
'portfolio':mod('portfolio_projects','Portfolio','معرض الأعمال','portfolio',[f('title','Project title',required=True),f('slug','URL slug',required=True),f('client_name','Public client name'),client,f('category','Category'),f('industry','Industry'),f('description','Description','textarea'),f('challenge','Challenge','textarea'),f('solution','Solution','textarea'),f('services_provided','Services provided (one per line)','textarea'),f('technologies','Technologies (one per line)','textarea'),f('results','Verified results','textarea'),f('project_date','Project date','date'),f('thumbnail_url','Thumbnail URL','url'),f('video_url','Video URL','url'),f('featured','Featured','boolean'),f('published','Published','boolean'),f('sort_order','Display order','number')]),
'portfolio-media':mod('portfolio_media','Portfolio images','صور الأعمال','portfolio',[f('portfolio_project_id','Portfolio project','relation',relation='portfolio_projects',required=True),f('url','Image URL','url',required=True),f('alt','Image description',required=True),f('sort_order','Order','number')]),
'content':mod('content_posts','Content calendar','تقويم المحتوى','marketing',[f('title','Content title',required=True),client,f('platform','Platform','select',options=['facebook','instagram','linkedin','tiktok','youtube','website','other']),f('content_type','Content type','select',options=['post','reel','story','article','video','other']),f('publishing_date','Publishing date','date'),f('caption','Caption','textarea'),f('hashtags','Hashtags'),f('designer_id','Designer','relation',relation='profiles'),f('copywriter_id','Copywriter','relation',relation='profiles'),f('editor_id','Video editor','relation',relation='profiles'),status(['idea','draft','in_production','review','scheduled','published'])]),
'campaigns':mod('marketing_campaigns','Campaigns','الحملات','marketing',[name,client,f('platform','Platform'),f('objective','Objective','textarea'),f('start_date','Start date','date'),f('end_date','End date','date'),f('budget_minor','Budget (EGP)','money'),f('ad_spend_minor','Ad spend (EGP)','money'),f('target_audience','Target audience','textarea'),status(['planned','active','paused','completed']),f('leads_generated','Leads generated','number'),f('engagement','Engagement','number'),f('reach','Reach','number'),f('conversions','Conversions','number'),f('results','Results','textarea'),notes]),
'social':mod('social_accounts','Social accounts','حسابات التواصل','marketing',[f('name','Account name',required=True),f('platform','Platform',required=True),f('url','Account URL','url',required=True),client,notes]),
'invoices':mod('invoices','Invoices','الفواتير','finance',[f('invoice_number','Invoice number',required=True),f('client_id','Client','relation',relation='clients',required=True),project,f('issue_date','Issue date','date',required=True),f('due_date','Due date','date',required=True),f('tax_bps','Tax (%)','percent'),notes],invoice=True),
'payments':mod('payments','Payments','المدفوعات','finance',[f('invoice_id','Invoice','relation',relation='invoices',required=True),f('amount_minor','Amount (EGP)','money',required=True),f('paid_at','Payment date','date',required=True),f('method','Method','select',options=['bank_transfer','cash','wallet','card','other']),f('reference','Reference'),notes]),
'expenses':mod('expenses','Expenses','المصروفات','finance',[f('name','Description',required=True),project,f('amount_minor','Amount (EGP)','money',required=True),f('category','Category'),f('expense_date','Date','date',required=True),notes]),
'files':mod('files','Files','الملفات','files',[f('name','File name',required=True),f('folder','Folder'),client,project]),
'notifications':mod('notifications','Notifications','الإشعارات','notifications',[f('title','Title'),f('body','Message'),f('read_at','Read at')],readOnly=True),
'activity':mod('activity_logs','Activity log','سجل النشاط','activity',[f('action','Action'),f('entity_table','Module'),f('entity_id','Record'),f('actor_id','Performed by'),f('created_at','Time')],readOnly=True),
'lead-activities':mod('lead_activities','Lead activity','متابعة الفرص','leads',[f('lead_id','Lead','relation',relation='leads',required=True),f('body','Activity note','textarea',required=True),f('kind','Activity type','select',options=['note','call','email','meeting','follow_up'])]),
'settings':mod('website_settings','Website settings','إعدادات الموقع','settings',[f('key','Setting key',required=True),f('value','Value','textarea',required=True),f('is_public','Public setting','boolean')]),
'testimonials':mod('testimonials','Testimonials','آراء العملاء','portfolio',[f('name','Client name',required=True),f('company','Company'),f('quote','Approved testimonial','textarea',required=True),f('published','Published','boolean')]),
'roles':mod('roles','Roles','الأدوار','security',[name,f('description','Description','textarea')],readOnly=True),
'permissions':mod('role_permissions','Role permissions','صلاحيات الأدوار','security',[f('role_id','Role','relation',relation='roles',required=True),f('permission_id','Permission','relation',relation='permissions',required=True)]),
}
(root/'src/lib/modules.ts').write_text('export type Field={key:string;label:string;type:string;required?:boolean;options?:string[];relation?:string;min?:number;max?:number};\nexport type Module={table:string;label:string;ar:string;permission:string;fields:Field[];statusKey?:string;readOnly?:boolean;noCreate?:boolean;invoice?:boolean};\nexport const modules:Record<string,Module>='+json.dumps(modules,ensure_ascii=False,indent=2)+';\nexport const tableLabel=(row:Record<string,unknown>)=>String(row.name??row.title??row.invoice_number??row.key??row.email??row.id??"Record");\n')
(root/'scripts/module-spec.json').write_text(json.dumps(modules,indent=2))
# Foundation SQL
sql='''-- HEXA PLUS relational foundation. No business/demo facts are inserted.
begin;
create extension if not exists pgcrypto;
create table public.roles(id uuid primary key default gen_random_uuid(),name text not null unique,description text,created_at timestamptz not null default now());
create table public.permissions(id uuid primary key default gen_random_uuid(),name text not null unique,description text);
create table public.role_permissions(id uuid primary key default gen_random_uuid(),role_id uuid not null references public.roles(id) on delete cascade,permission_id uuid not null references public.permissions(id) on delete cascade,unique(role_id,permission_id),created_at timestamptz not null default now());
create table public.departments(id uuid primary key default gen_random_uuid(),name text not null unique,created_at timestamptz not null default now(),updated_at timestamptz not null default now(),created_by uuid references auth.users(id) on delete set null,updated_by uuid references auth.users(id) on delete set null);
create table public.profiles(id uuid primary key references auth.users(id) on delete cascade,name text not null,email text not null,phone text,job_title text,avatar_path text,department_id uuid references public.departments(id) on delete set null,joining_date date, status text not null default 'active' check(status in ('active','inactive')),role_id uuid references public.roles(id) on delete restrict,created_at timestamptz not null default now(),updated_at timestamptz not null default now(),created_by uuid references auth.users(id) on delete set null,updated_by uuid references auth.users(id) on delete set null);
create or replace function public.is_super_admin() returns boolean language sql stable security definer set search_path='' as $$select exists(select 1 from public.profiles p join public.roles r on r.id=p.role_id where p.id=auth.uid() and p.status='active' and r.name='super_admin')$$;
create or replace function public.has_permission(requested text) returns boolean language sql stable security definer set search_path='' as $$select exists(select 1 from public.profiles p join public.roles r on r.id=p.role_id left join public.role_permissions rp on rp.role_id=r.id left join public.permissions pe on pe.id=rp.permission_id where p.id=auth.uid() and p.status='active' and (r.name='super_admin' or pe.name=requested))$$;
revoke all on function public.has_permission(text),public.is_super_admin() from public;
grant execute on function public.has_permission(text),public.is_super_admin() to authenticated;
'''
base="id uuid primary key default gen_random_uuid(),created_at timestamptz not null default now(),updated_at timestamptz not null default now(),created_by uuid references auth.users(id) on delete set null,updated_by uuid references auth.users(id) on delete set null"
# References must be created in dependency order.
order=['clients','leads','projects','milestones','tasks','comments','project-members','services','portfolio','portfolio-media','content','campaigns','social','invoices','payments','expenses','files','notifications','activity','lead-activities','settings','testimonials']
references={'account_manager_id':'profiles','assigned_to':'profiles','manager_id':'profiles','designer_id':'profiles','copywriter_id':'profiles','editor_id':'profiles','actor_id':'profiles'}
for key in order:
 m=modules[key];cols=[]
 for field in m['fields']:
  k,t=field['key'],field['type']
  if k in ['id','created_at','updated_at','created_by','updated_by']:continue
  if t=='relation' or k in references:
   target=field.get('relation',references.get(k)); cols.append(f'{k} uuid references public.{target}(id) on delete '+('restrict' if field.get('required') else 'set null')+(' not null' if field.get('required') else ''))
  elif t=='boolean':cols.append(f'{k} boolean not null default false')
  elif t in ['money','number','percent']:
   default='0';check=f'{k} >= 0';check+=f' and {k} <= {field["max"]}' if 'max' in field else '';cols.append(f'{k} bigint not null default {default} check({check})')
  elif t=='date':cols.append(f'{k} date'+(' not null' if field.get('required') else ''))
  else:
   c=f'{k} text'; c+= ' not null' if field.get('required') else '';c+=f" default '{field['options'][0]}' check({k} in ("+','.join("'"+v+"'" for v in field['options'])+'))' if t=='select' else '';cols.append(c)
 if key=='invoices':cols+=['subtotal_minor bigint not null default 0 check(subtotal_minor>=0)','tax_minor bigint not null default 0 check(tax_minor>=0)','total_minor bigint not null default 0 check(total_minor>=0)'];cols+=['unique(invoice_number)']
 if key in ['services','portfolio']:cols+=['unique(slug)']
 if key=='files':cols+=['storage_path text not null unique','mime_type text not null','size_bytes bigint not null check(size_bytes>=0)']
 if key=='notifications':cols+=['recipient_id uuid references public.profiles(id) on delete cascade','link text']
 if key=='activity':cols+=['changes jsonb not null default \'{}\'::jsonb']
 if key=='settings':cols+=['unique(key)']
 if key=='project-members':cols+=['unique(project_id,profile_id)']
 sql+=f'create table public.{m["table"]}('+base+','+','.join(cols)+');\n'
sql+='''create table public.invoice_items(id uuid primary key default gen_random_uuid(),invoice_id uuid not null references public.invoices(id) on delete cascade,description text not null,quantity integer not null check(quantity between 1 and 100000),unit_price_minor bigint not null check(unit_price_minor between 0 and 100000000),sort_order integer not null default 0);
create table public.task_attachments(id uuid primary key default gen_random_uuid(),task_id uuid not null references public.tasks(id) on delete cascade,file_id uuid not null references public.files(id) on delete cascade,created_at timestamptz not null default now(),unique(task_id,file_id));
create table public.contact_submissions(id uuid primary key default gen_random_uuid(),lead_id uuid not null references public.leads(id) on delete cascade,consent boolean not null default true,created_at timestamptz not null default now());
create or replace function public.stamp_record() returns trigger language plpgsql security definer set search_path='' as $$ begin
 if TG_OP='INSERT' then NEW.created_by=auth.uid();end if;NEW.updated_at=now();NEW.updated_by=auth.uid();return NEW;end;$$;
create or replace function public.log_change() returns trigger language plpgsql security definer set search_path='' as $$ begin
 insert into public.activity_logs(action,entity_table,entity_id,actor_id,changes) values(lower(TG_OP),TG_TABLE_NAME,coalesce(NEW.id,OLD.id)::text,auth.uid(),jsonb_build_object('record',coalesce(NEW.id,OLD.id)));
 return coalesce(NEW,OLD);end;$$;
'''
tables=list(dict.fromkeys(m['table'] for m in modules.values()))+['invoice_items','task_attachments','contact_submissions','permissions']
for table in tables:
 sql+=f'alter table public.{table} enable row level security;\n'
 if table not in ['roles','permissions','role_permissions','invoice_items','task_attachments','contact_submissions']:
  sql+=f'create trigger stamp before insert or update on public.{table} for each row execute function public.stamp_record();\n'
 if table not in ['activity_logs','notifications','contact_submissions']:
  sql+=f'create trigger audit after insert or update or delete on public.{table} for each row execute function public.log_change();\n'
 sql+=f'create index if not exists {table}_created_idx on public.{table}(created_at desc);\n' if table not in ['permissions','invoice_items'] else ''
# Security tables cannot be used by a non-super-admin to upgrade access.
for table in ['roles','permissions']:
 sql+=f"create policy authenticated_read on public.{table} for select to authenticated using(true);\ncreate policy super_manage on public.{table} for all to authenticated using(public.is_super_admin()) with check(public.is_super_admin());\n"
sql+="create policy role_permissions_read on public.role_permissions for select to authenticated using(public.is_super_admin() or role_id=(select role_id from public.profiles where id=auth.uid()));\ncreate policy super_manage on public.role_permissions for all to authenticated using(public.is_super_admin()) with check(public.is_super_admin());\n"
for k,m in modules.items():
 t=m['table'];perm=m['permission']
 if t in ['roles','role_permissions']:continue
 read=f"public.has_permission('{perm}.read')"
 if t=='profiles':read=f'(id=auth.uid() or {read})'
 if t=='tasks':read=f"({read} and (assigned_to=auth.uid() or public.has_permission('tasks.write')))"
 if t=='projects':read=f"({read} and (manager_id=auth.uid() or public.has_permission('projects.write') or exists(select 1 from public.project_members pm where pm.project_id=id and pm.profile_id=auth.uid())))"
 if t=='notifications':read='(recipient_id=auth.uid())'
 sql+=f'create policy module_read on public.{t} for select to authenticated using({read});\n'
 if m.get('readOnly'):continue
 write="public.is_super_admin()" if t=='profiles' else f"public.has_permission('{perm}.write')"
 for action in ['insert','update','delete']:
  sql+=f'create policy module_{action} on public.{t} for {action} to authenticated '+(f'with check({write})' if action=='insert' else f'using({write})'+(f' with check({write})' if action=='update' else ''))+';\n'
for table,expression in [('services','published=true'),('portfolio_projects','published=true'),('portfolio_media','exists(select 1 from public.portfolio_projects p where p.id=portfolio_project_id and p.published=true)'),('testimonials','published=true'),('website_settings','is_public=true')]:
 sql+=f'create policy public_read on public.{table} for select to anon,authenticated using({expression});\n'
for table,perm in [('invoice_items','finance'),('task_attachments','tasks'),('contact_submissions','leads')]:
 sql+=f"create policy module_read on public.{table} for select to authenticated using(public.has_permission('{perm}.read'));\n"
 if table!='contact_submissions':sql+=f"create policy module_write on public.{table} for all to authenticated using(public.has_permission('{perm}.write')) with check(public.has_permission('{perm}.write'));\n"
# Index every foreign key and operational filter.
for m in modules.values():
 for f in m['fields']:
  if f['type'] in ['relation','date','select']:
   sql+=f'create index if not exists {m["table"]}_{f["key"]}_idx on public.{m["table"]}({f["key"]});\n'
sql+='''create index invoice_items_invoice_idx on public.invoice_items(invoice_id);
create index notifications_recipient_idx on public.notifications(recipient_id);
create index activity_actor_idx on public.activity_logs(actor_id);
create or replace function public.submit_inquiry(payload jsonb) returns uuid language plpgsql security definer set search_path='' as $$
declare lid uuid; person text; email_value text; begin
person=btrim(payload->>'name'); email_value=lower(btrim(payload->>'email'));
if person is null or length(person)<2 or length(person)>200 or email_value is null or email_value !~ '^[^[:space:]@]+@[^[:space:]@]+\\.[^[:space:]@]+$' or length(email_value)>254 or length(coalesce(payload->>'description','')) not between 20 and 10000 then raise exception 'Please check your name, email and project description.';end if;
perform pg_advisory_xact_lock(hashtext(email_value));
if (select count(*) from public.leads where lower(email)=email_value and created_at>now()-interval '1 hour')>=3 then raise exception 'Please wait before sending another inquiry.';end if;
insert into public.leads(name,company,email,phone,service,budget,timeline,description,source,stage) values(person,left(payload->>'company',200),email_value,left(payload->>'phone',80),left(payload->>'service',200),left(payload->>'budget',100),left(payload->>'timeline',100),payload->>'description','website','new') returning id into lid;
insert into public.contact_submissions(lead_id) values(lid);
insert into public.notifications(recipient_id,title,body,link) select p.id,'New project inquiry',person||' sent a project inquiry.','/dashboard/leads/'||lid from public.profiles p join public.roles r on r.id=p.role_id where p.status='active' and (r.name='super_admin' or exists(select 1 from public.role_permissions rp join public.permissions pe on pe.id=rp.permission_id where rp.role_id=r.id and pe.name='leads.read'));
return lid;end;$$;
revoke all on function public.submit_inquiry(jsonb) from public;
grant execute on function public.submit_inquiry(jsonb) to anon,authenticated;
-- A single transaction updates invoice lines and totals. Money is integer minor units.
create or replace function public.save_invoice(record_id uuid,header jsonb,items jsonb) returns uuid language plpgsql security invoker set search_path='' as $$
declare iid uuid; line jsonb; subtotal bigint:=0; tax bigint; rate integer;begin
if not public.has_permission('finance.write') then raise exception 'Permission denied';end if;
if jsonb_typeof(items)!='array' or jsonb_array_length(items) not between 1 and 100 then raise exception 'Add 1 to 100 invoice items';end if;
rate=coalesce((header->>'tax_bps')::integer,0);if rate not between 0 and 10000 then raise exception 'Invalid tax rate';end if;
for line in select * from jsonb_array_elements(items) loop
if length(btrim(line->>'description')) not between 1 and 500 or (line->>'quantity')::integer not between 1 and 100000 or (line->>'unit_price_minor')::bigint not between 0 and 100000000 then raise exception 'Invalid invoice item';end if;
subtotal=subtotal+(line->>'quantity')::integer*(line->>'unit_price_minor')::bigint;end loop;
if subtotal>9007199254740991 then raise exception 'Invoice total too large';end if;
tax=round(subtotal::numeric*rate/10000)::bigint;
if record_id is null then
insert into public.invoices(invoice_number,client_id,project_id,issue_date,due_date,tax_bps,notes,subtotal_minor,tax_minor,total_minor) values(header->>'invoice_number',(header->>'client_id')::uuid,nullif(header->>'project_id','')::uuid,(header->>'issue_date')::date,(header->>'due_date')::date,rate,header->>'notes',subtotal,tax,subtotal+tax) returning id into iid;
else iid=record_id;perform 1 from public.invoices where id=iid for update;if not found then raise exception 'Invoice not found';end if;
if exists(select 1 from public.payments where invoice_id=iid) then raise exception 'Invoices with payments cannot be edited';end if;
update public.invoices set invoice_number=header->>'invoice_number',client_id=(header->>'client_id')::uuid,project_id=nullif(header->>'project_id','')::uuid,issue_date=(header->>'issue_date')::date,due_date=(header->>'due_date')::date,tax_bps=rate,notes=header->>'notes',subtotal_minor=subtotal,tax_minor=tax,total_minor=subtotal+tax where id=iid;
delete from public.invoice_items where invoice_id=iid;end if;
insert into public.invoice_items(invoice_id,description,quantity,unit_price_minor,sort_order) select iid,v->>'description',(v->>'quantity')::integer,(v->>'unit_price_minor')::bigint,(ord-1)::integer from jsonb_array_elements(items) with ordinality as t(v,ord);
return iid;end;$$;
revoke all on function public.save_invoice(uuid,jsonb,jsonb) from public;
grant execute on function public.save_invoice(uuid,jsonb,jsonb) to authenticated;
-- Prevent accidental overpayment even with concurrent requests.
create or replace function public.validate_payment() returns trigger language plpgsql set search_path='' as $$declare invoice_total bigint;other_paid bigint;begin
select total_minor into invoice_total from public.invoices where id=NEW.invoice_id for update;
select coalesce(sum(amount_minor),0) into other_paid from public.payments where invoice_id=NEW.invoice_id and id<>NEW.id;
if NEW.amount_minor<=0 or other_paid+NEW.amount_minor>invoice_total then raise exception 'Payment must be positive and cannot exceed the outstanding amount';end if;return NEW;end;$$;
create trigger check_payment before insert or update on public.payments for each row execute function public.validate_payment();
create or replace function public.notify_task() returns trigger language plpgsql security definer set search_path='' as $$begin
if NEW.assigned_to is not null and (TG_OP='INSERT' or NEW.assigned_to is distinct from OLD.assigned_to) then insert into public.notifications(recipient_id,title,body,link) values(NEW.assigned_to,'Task assigned',NEW.title,'/dashboard/tasks/'||NEW.id);end if;return NEW;end;$$;
create trigger task_notify after insert or update on public.tasks for each row execute function public.notify_task();
create or replace function public.set_task_status(task uuid,next_status text) returns void language plpgsql security definer set search_path='' as $$begin
if next_status not in ('to_do','in_progress','in_review','completed') then raise exception 'Invalid status';end if;
if not(public.has_permission('tasks.write') or (public.has_permission('tasks.status') and exists(select 1 from public.tasks where id=task and assigned_to=auth.uid()))) then raise exception 'Permission denied';end if;
update public.tasks set status=next_status where id=task;end;$$;
revoke all on function public.set_task_status(uuid,text) from public;
grant execute on function public.set_task_status(uuid,text) to authenticated;
-- Private storage. Public portfolio media is published intentionally to a separate bucket.
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values('business-files','business-files',false,10485760,array['image/jpeg','image/png','image/webp','application/pdf','text/plain','text/csv','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']),('portfolio','portfolio',true,10485760,array['image/jpeg','image/png','image/webp']) on conflict(id) do nothing;
create policy business_files_read on storage.objects for select to authenticated using(bucket_id='business-files' and public.has_permission('files.read'));
create policy business_files_insert on storage.objects for insert to authenticated with check(bucket_id='business-files' and public.has_permission('files.write'));
create policy business_files_delete on storage.objects for delete to authenticated using(bucket_id='business-files' and public.has_permission('files.write'));
create policy portfolio_read on storage.objects for select to anon,authenticated using(bucket_id='portfolio');
create policy portfolio_insert on storage.objects for insert to authenticated with check(bucket_id='portfolio' and public.has_permission('portfolio.write'));
create policy portfolio_delete on storage.objects for delete to authenticated using(bucket_id='portfolio' and public.has_permission('portfolio.write'));
insert into public.roles(name,description) values('super_admin','Full access, including permissions and account roles'),('admin','Business administration'),('project_manager','Delivery and team coordination'),('marketing_manager','Marketing and public content'),('team_member','Assigned delivery work'),('sales_crm_manager','CRM and lead pipeline');
'''
perms=sorted(set(m['permission'] for m in modules.values()))
for perm in perms:
 for action in ['read','write']:sql+=f"insert into public.permissions(name) values('{perm}.{action}');\n"
sql+="insert into public.permissions(name) values('tasks.status');\n"
grants={
 'admin':[p+'.'+a for p in perms if p not in ['security'] for a in ['read','write'] if not(p=='team' and a=='write')],
 'project_manager':['clients.read','projects.read','projects.write','tasks.read','tasks.write','files.read','files.write','team.read','activity.read'],
 'marketing_manager':['clients.read','marketing.read','marketing.write','services.read','services.write','portfolio.read','portfolio.write','files.read','files.write','team.read'],
 'team_member':['projects.read','tasks.read','tasks.status','team.read'],
 'sales_crm_manager':['clients.read','clients.write','leads.read','leads.write','projects.read','team.read']}
for role,pg in grants.items():
 for p in pg:sql+=f"insert into public.role_permissions(role_id,permission_id) select r.id,p.id from public.roles r,public.permissions p where r.name='{role}' and p.name='{p}';\n"
for dept in ['Development','Marketing','Design','Video Production','Sales','Management']:sql+=f"insert into public.departments(name) values('{dept}');\n"
sql+='''-- Never expose the service-role key to browser bundles. Anonymous roles only have the explicit policies above.
commit;
'''
(root/'supabase/migrations/202611210001_foundation.sql').write_text(sql)
print('Generated',len(modules),'module definitions and',len(sql),'bytes of foundation SQL')
