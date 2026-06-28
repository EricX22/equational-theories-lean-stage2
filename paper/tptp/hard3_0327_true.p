% hard3_0327  eq1=3062 eq2=1462  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(X,X),Y),Z),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(Z,f(X,Y))) )).
