% hard3_0308  eq1=2884 eq2=2045  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),X),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,X),Y),f(Y,Z)) )).
