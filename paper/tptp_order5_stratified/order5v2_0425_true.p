% order5v2_0425  eq1=41173 eq2=3600  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),X),X),W),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(Z,f(f(Y,X),Y)) )).
