% order5v2_0898  eq1=32340 eq2=33143  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,Y)),W)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(f(Y,X),Z),Z)),Z) )).
