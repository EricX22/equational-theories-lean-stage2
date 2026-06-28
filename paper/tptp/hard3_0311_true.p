% hard3_0311  eq1=2892 eq2=4119  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Z),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,X),X),Z) )).
