% hard3_0219  eq1=2059 eq2=3077  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),X),f(Z,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Y),X),Z) )).
