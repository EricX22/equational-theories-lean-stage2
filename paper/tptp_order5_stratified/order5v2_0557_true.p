% order5v2_0557  eq1=23928 eq2=57599  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(W,f(X,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,X)) = f(f(f(Z,X),Y),W) )).
