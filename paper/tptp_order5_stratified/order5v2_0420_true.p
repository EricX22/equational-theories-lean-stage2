% order5v2_0420  eq1=31403 eq2=924  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,Y),f(X,Z))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Y,Y),f(Z,Z))) )).
