% hard3_0388  eq1=4204 eq2=395  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,X),W),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,X),Y) )).
