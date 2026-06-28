% hard3_0297  eq1=2831 eq2=2060  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Z)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,Y),Y),f(X,X)) )).
