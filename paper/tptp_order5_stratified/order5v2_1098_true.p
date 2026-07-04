% order5v2_1098  eq1=32288 eq2=8958  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Y,Y)),Y)),Z) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(f(W,X),W),U))) )).
