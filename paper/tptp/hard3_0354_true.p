% hard3_0354  eq1=3360 eq2=379  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Y,f(Y,f(Z,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,Y),Z) )).
