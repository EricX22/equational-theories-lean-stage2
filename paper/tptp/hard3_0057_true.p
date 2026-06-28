% hard3_0057  eq1=372 eq2=315  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(Y,Z),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(Y,f(Y,X)) )).
