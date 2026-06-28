% hard3_0338  eq1=3171 eq2=4480  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,Y)) = f(f(Y,X),Y) )).
